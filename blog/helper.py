from django.core.mail import send_mail
from django.conf import settings


def send_forgot_password(email,token):
    subject="Password Change - Interview Blog"
    message = f'Hi, Click on the given link to change your password http://127.0.0.1:8000/changepass/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject,message,email_from,recipient_list)
    return True