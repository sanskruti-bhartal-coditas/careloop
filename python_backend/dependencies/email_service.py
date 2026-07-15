import boto3
from botocore.exceptions import ClientError
from config import settings
ses_client = boto3.client(
    "ses",
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name="ap-south-1"
)


class EmailService:
    @staticmethod
    def send_email(to_email: str,subject: str,html_body: str):
        ses_identity_arn = "arn:aws:ses:ap-south-1:804372444763:identity/suyogdhage@gmail.com"   
        try:
            response = ses_client.send_email(Source=settings.EMAILS_FROM_EMAIL,SourceArn=ses_identity_arn,  Destination={"ToAddresses": [to_email]},
    Message={"Subject": {"Data": subject},"Body": {"Html": {"Data": html_body}}})


        except ClientError as e:
            raise Exception(
                f"SES email failed: {e.response['Error']['Message']}")

    @staticmethod
    def send_invite(to_email: str,token: str,subject: str,message: str,) :
        link = (
            f"{settings.FRONTEND_URL}"
            f"/reset-password?token={token}")

        html = f"""
        <p>{message}</p>
        <p>
            <a href="{link}">
                Set Password
            </a>
        </p>
        """
        EmailService.send_email(to_email=to_email,subject=subject,html_body=html)


email_service = EmailService()
