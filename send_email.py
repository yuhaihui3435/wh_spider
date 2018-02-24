from email.mime.text import MIMEText
import smtplib

def sendEmail(msg):
    fro="yuhaihui8913@163.com"
    pwd="zhengwei617"
    to=["125227112@qq.com"]
    smtp="smtp.163.com"
    title = '程序提醒'  # 邮件主题
    msg = MIMEText(msg, 'plain', 'utf-8')
    msg['From'] = "{}".format(fro)
    msg['To'] = ",".join(to)
    msg['Subject'] = title
    server = smtplib.SMTP(smtp, 25)  # SMTP协议默认端口是25
    try:
        server.set_debuglevel(1)
        server.login(fro, pwd)
        server.sendmail(fro, [to], msg.as_string())

    except smtplib.SMTPException as e:
        print(e)
    finally:
        server.quit()
if __name__ == '__main__':
    sendEmail('已经ok')