import cv2
from AipOcr import VCodeRec


def get_vercode(wd, captchaImg):
    """
    注意：在非 headless 模式中，请将显示设置中的缩放设置调到 100%
    :param wd: webdriver对象，代表整个网页
    :param captchaImg: 验证码对象
    :return: 验证码识别结果
    """
    wd.set_window_size(1920, 1080)
    wd.save_screenshot('data/screenshot.png')

    location = captchaImg.location
    size = captchaImg.size

    x1 = location['x']
    x2 = location['x'] + size['width']
    y1 = location['y']
    y2 = location['y'] + size['height']

    img = cv2.imread('data/screenshot.png', 1)
    img = img[y1:y2, x1:x2, :]
    cv2.imwrite("data/captcha.jpg", img)

    word = VCodeRec('data/captcha.jpg')
    return word
