import os
import boto3
from botocore.exceptions import ClientError
from .base import BaseEmailProvider

class SESProvider(BaseEmailProvider):
    def __init__(self):
        self.aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
        self.aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        self.region = os.getenv("AWS_REGION", "us-east-1")
        if not all([self.aws_access_key, self.aws_secret_key]):
            raise RuntimeError("AWS credentials not set")

        self.client = boto3.client(
            "ses",
            region_name=self.region,
            aws_access_key_id=self.aws_access_key,
            aws_secret_access_key=self.aws_secret_key,
        )

    def send_email(self, subject: str, to_email: str, from_email: str,
                   plain_text: str, html_content: str) -> bool:
        try:
            response = self.client.send_email(
                Source=from_email,
                Destination={"ToAddresses": [to_email]},
                Message={
                    "Subject": {"Data": subject},
                    "Body": {
                        "Text": {"Data": plain_text},
                        "Html": {"Data": html_content},
                    },
                },
            )
            return response["ResponseMetadata"]["HTTPStatusCode"] == 200
        except ClientError as e:
            print(f"SES send_email error: {e.response['Error']['Message']}")
            return False
