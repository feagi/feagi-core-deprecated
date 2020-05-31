# Copyright (c) 2019 Mohammad Nadji-Tehrani <m.nadji.tehrani@gmail.com>
#!/usr/bin/python -tt

from email.mime.text import MIMEText
from datetime import date
import smtplib

with open('../code.txt', 'r') as the_code:
    code = the_code.read()

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USERNAME = "MNT.FEAGI@gmail.com"
SMTP_PASSWORD = ""

EMAIL_TO = ["MNT.FEAGI@gmail.com"]
EMAIL_FROM = "MNT.FEAGI@gmail.com"
EMAIL_SUBJECT = "FEAGI report"

DATE_FORMAT = "%d/%m/%Y"
EMAIL_SPACE = ", "

DATA = "FEAGI's first email"


def send_email(mail_body):
    msg = MIMEText(mail_body)
    msg['Subject'] = EMAIL_SUBJECT + " %s" % (date.today().strftime(DATE_FORMAT))
    msg['To'] = EMAIL_SPACE.join(EMAIL_TO)
    msg['From'] = EMAIL_FROM
    mail = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    mail.starttls()
    mail.login(SMTP_USERNAME, SMTP_PASSWORD)
    mail.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())
    mail.quit()


if __name__=='__main__':
    send_email("FEAGI's second")