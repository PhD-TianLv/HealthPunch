# %%
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
import Settings as settings
from VerCode import get_vercode
from Mail import send_mails
import random
import json
import time
import os

# 谷歌浏览器设置项
chrome_options = Options()
# 这三行代表设置 chrome 为无界面，方便 linux 服务器使用，windows 端调试时可以注释掉
chrome_options.add_argument('--headless')
chrome_options.add_argument('--hide-scrollbars')
chrome_options.add_argument('--no-sandbox')

chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('window-size=1920x1080')

for user in settings.user_info:
    # 启动谷歌浏览器
    wd = webdriver.Chrome(options=chrome_options)
    wd.implicitly_wait(10)

    # 统一身份认证登录
    for _ in range(10):  # 尝试登录
        wd.get(settings.url)
        captchaImg = wd.find_element_by_xpath('//form[@id="casLoginForm"]//img[@id="captchaImg"]')
        ver_code = get_vercode(wd, captchaImg)
        if len(ver_code) != 4:
            continue

        username_input = wd.find_element_by_xpath('//form[@id="casLoginForm"]//input[@id="username"]')
        password_input = wd.find_element_by_xpath('//form[@id="casLoginForm"]//input[@id="password"]')
        captcha_input = wd.find_element_by_xpath('//form[@id="casLoginForm"]//input[@id="captchaResponse"]')
        login_button = wd.find_element_by_xpath('//form[@id="casLoginForm"]//button[@type="submit"]')

        username_input.clear()
        password_input.clear()
        captcha_input.clear()

        username_input.send_keys(settings.username_info[user])
        password_input.send_keys(settings.password_info[user])
        captcha_input.send_keys(ver_code)
        login_button.click()

        # 如果成功进入每日健康打卡界面，则退出循环
        if wd.title == '健康上报平台':
            print(user + "成功进入每日健康打卡界面！")
            break

    if wd.title != '健康上报平台':
        print(user + '登录失败！')
        settings.result_text[user] = '综合服务门户密码错误！\n每日健康打卡未能完成！'
        continue

    while wd.find_elements_by_xpath('//div[@class="weui_media_bd"]') \
            and wd.find_element_by_xpath('//div[@class="weui_media_bd"]').text == '江苏大学疫情防控':
        wd.find_element_by_xpath('//a[@class="weui_btn  weui_btn_primary"]').click()

    # 随机生成体温
    temper1_input = wd.find_element_by_xpath('//input[@id="xwwd"]')
    temper2_input = wd.find_element_by_xpath('//input[@id="swwd"]')

    temper1_input.clear()
    temper2_input.clear()

    temper1_input.send_keys(str(random.randint(360, 370) / 10))
    temper2_input.send_keys(str(random.randint(360, 370) / 10))

    # 其他异常
    other_symptoms_select = Select(wd.find_element_by_xpath('//select[@id="qtyc"]'))
    other_symptoms_select.select_by_value("无")

    wd.find_element_by_xpath('//button[@id="button1"]').click()

    # 获取结果
    text = wd.find_element_by_xpath('//div[@class="weui_media_bd"]').text
    settings.result_text[user] = text

    # 退出
    wd.quit()
    print(user + '打卡任务已完成！')

# 结果文件写入
result_name = time.strftime('%Y-%m-%d') + '.json'
result_path = os.path.join('results', result_name)
with open(result_path, 'w') as f:
    json.dump(settings.result_text, f)

# 发送邮件，通知用户
send_mails(result_path)
print('邮件已发送完毕')



#在不允许发送邮件的云服务器上,使用一下函数提供确认功能
temp=open("log.txt", mode='a+')
temp.write("\n----------------------------\n当前时间为:"+time.asctime( time.localtime(time.time()) )+"\n打卡任务已完成！\n----------------------------\n")
temp.close()
