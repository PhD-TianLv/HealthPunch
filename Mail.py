# %%
import smtplib
from email.header import Header
from email.mime.text import MIMEText
import Settings as settings
import json


def send_mails(result_path):
    data = json.load(open(result_path))

    for user in settings.user_info:
        content = data[user]
        title = '自动健康打卡'

        message = MIMEText(content, 'plain', 'utf-8')
        message['From'] = "{}".format(settings.sender)
        message['To'] = ",".join(settings.receivers_info[user])
        message['Subject'] = title

        smtpObj = smtplib.SMTP_SSL(settings.mail_host, 465)
        smtpObj.login(settings.mail_user, settings.mail_pass)
        smtpObj.sendmail(settings.sender, settings.receivers_info[user], message.as_string())