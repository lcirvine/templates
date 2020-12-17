import os
import logging
from datetime import date
import configparser
import win32com.client as win32


log_folder = os.path.join(os.getcwd(), 'Logs')
log_file = os.path.join(log_folder, 'Log File.txt')
today_date = date.today().strftime('%Y-%m-%d')

if not os.path.exists(log_folder):
    os.mkdir(log_folder)
handler = logging.FileHandler(os.path.join(log_folder, log_file), mode='a+', encoding='UTF-8')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger = logging.getLogger()
logger.addHandler(handler)
logger.setLevel(logging.INFO)
logger.info('-' * 100)


def error_email(error_message: str = ''):
    """
    Used to send an email when an error is encountered.
    Email details like sender and recipients are provided in .ini file which is read by configparser.
    :param error_message: optional string that will be added to body of email
    :return:
    """
    config = configparser.ConfigParser()
    config.read('email_settings.ini')
    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)
    mail.To = config.get('Email', 'ErrorTo')
    mail.Sender = config.get('Email', 'Sender')
    mail.Subject = f"ERROR: {config.get('Email', 'Subject')} {today_date}"
    mail.HTMLBody = config.get('Email', 'ErrorBody') + error_message + config.get('Email', 'Signature')
    mail.Attachments.Add(log_file)
    mail.Send()
