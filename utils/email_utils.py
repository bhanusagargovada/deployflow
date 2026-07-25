import smtplib
from email.message import EmailMessage
from flask import current_app


def send_email(subject: str, recipients: list, body: str):
    mail_server = current_app.config.get('MAIL_SERVER')
    mail_port = current_app.config.get('MAIL_PORT')
    mail_user = current_app.config.get('MAIL_USERNAME')
    mail_pass = current_app.config.get('MAIL_PASSWORD')

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = mail_user or 'noreply@example.com'
    msg['To'] = ','.join(recipients)
    msg.set_content(body)

    if not mail_server:
        # Fallback: print to console
        print('--- EMAIL (console) ---')
        print('To:', recipients)
        print('Subject:', subject)
        print(body)
        print('--- END EMAIL ---')
        return True

    try:
        with smtplib.SMTP(mail_server, mail_port) as s:
            s.starttls()
            if mail_user and mail_pass:
                s.login(mail_user, mail_pass)
            s.send_message(msg)
        return True
    except Exception as e:
        print('Email send failed:', e)
        return False
