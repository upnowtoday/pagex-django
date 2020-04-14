from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string


def send_email_verification(verification):
    ctx = {
        'email_verification_code': verification.code
    }

    message = render_to_string('author/auth/verification_code_email.html', context=ctx)
    mail_kwargs = {
        'subject': 'Your verification code at PageX',
        'message': message,
        'from_email': settings.DEFAULT_FROM_EMAIL,
        'recipient_list': [verification.email],
        'html_message': message
    }
    send_mail(**mail_kwargs)
