import os
import sys
from datetime import date
import configparser
import win32com.client as win32
# from project_logging import logger, error_email

config = configparser.ConfigParser()
config.read('email_settings.ini')
today_date = date.today().strftime('%Y-%m-%d')


def email_report(attach_file, addtl_message: str = ''):
    """
    Emails the report as an attachment.
    Email details like sender and recipients are provided in .ini file which is read by configparser.
    :param attach_file: path of a file or list of files which will be attached to the email
    :param addtl_message: optional string that can be added to body of email
    :return: None
    """
    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)
    mail.To = config.get('Email', 'To')
    mail.Sender = config.get('Email', 'Sender')
    mail.Subject = f"{config.get('Email', 'Subject')} {today_date}"
    mail.HTMLBody = config.get('Email', 'Body') + addtl_message + config.get('Email', 'Signature')
    if isinstance(attach_file, str) and os.path.exists(attach_file):
        mail.Attachments.Add(attach_file)
    elif isinstance(attach_file, list):
        for f in attach_file:
            mail.Attachments.Add(f)
    mail.Send()
    # logger.info(f"Email sent to {config.get('Email', 'Subject')}")


def main():
    try:
        email_report(os.path.join('Results', 'SPAC IPOs.xlsx'))
    except Exception as e:
        # logger.error(e, exc_info=sys.exc_info())
        # error_email(str(e))
        # logger.info('-' * 100)


if __name__ == '__main__':
    main()