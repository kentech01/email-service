import os
from typing import Optional
import boto3
from botocore.exceptions import ClientError
from .base import BaseEmailProvider


class SESProvider(BaseEmailProvider):
    def __init__(self):
        self.aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
        self.aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        self.region = os.getenv("AWS_REGION")
        if not all([self.aws_access_key, self.aws_secret_key]):
            raise RuntimeError("AWS credentials not set")

        self.client = boto3.client(
            "ses",  # v1 is OK; you can switch to "sesv2" later
            region_name=self.region,
            aws_access_key_id=self.aws_access_key,
            aws_secret_access_key=self.aws_secret_key,
        )

    def send_email(
        self,
        subject: str,
        to_email: str,
        from_email: str,
        plain_text: str,
        html_content: str,
        reply_to: Optional[str] = None,
    ) -> bool:
        try:
            params = {
                "Source": from_email,
                "Destination": {"ToAddresses": [to_email]},
                "Message": {
                    "Subject": {"Data": subject, "Charset": "UTF-8"},
                    "Body": {
                        "Text": {"Data": plain_text, "Charset": "UTF-8"},
                        "Html": {"Data": html_content, "Charset": "UTF-8"},
                    },
                },
            }
            if reply_to:
                params["ReplyToAddresses"] = [reply_to]

            response = self.client.send_email(**params)
            return response["ResponseMetadata"]["HTTPStatusCode"] == 200
        except ClientError as e:
            print(f"SES send_email error: {e.response['Error']['Message']}")
            return False
