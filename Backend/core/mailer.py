
import smtplib
from email.message import EmailMessage
from core.config import Settings

settings = Settings()



class Mailer:
    
    @staticmethod
    def send_message(content: str, subject: str, mail_to: str):
        message = EmailMessage()
        message.set_content(content)
        message['Subject'] = subject
        message['From'] = settings.EMAIL_HOST_USER
        message['To'] = mail_to
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        server.send_message(message)
        print('E-mail has been sent!')
        server.quit()



    @staticmethod
    def send_confirmation_message(token: str, mail_to: str):
        confirmation_url = f'http://localhost:8000/api/verify/{token}'
        message = '''Hi!
    Please confirm your registration: {}'''.format(confirmation_url)
        Mailer.send_message(
            message,
            'Please confirm your registration',
            mail_to
        )