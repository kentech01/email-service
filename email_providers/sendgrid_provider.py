import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email
from .base import BaseEmailProvider

class SendGridProvider(BaseEmailProvider):
    def __init__(self):
        self.api_key = os.getenv("SENDGRID_API_KEY")
        if not self.api_key:
            raise RuntimeError("SENDGRID_API_KEY is not set")

    def send_email(self, subject: str, to_email: str, from_email: str,
                plain_text: str, html_content: str, reply_to: str = None) -> bool:

        message = Mail(
            from_email=from_email,
            to_emails=to_email,
            subject=subject,
            plain_text_content=plain_text,
            html_content=html_content,
        )

        if reply_to:
            message.reply_to = Email(reply_to)

        try:
            sg = SendGridAPIClient(self.api_key)
            response = sg.send(message)
            return response.status_code < 400
        except Exception as e:
            print(f"SendGrid send_email error: {e}")
            return False
