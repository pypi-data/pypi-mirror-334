import boto3
from django.conf import settings
from botocore.exceptions import ClientError

""" """
class SNSNotification:
    def __init__(self):
        """Creating an AWS SNS Client"""
        self.client = boto3.client(
            'sns',
            region_name='us-east-1'
        )
        self.topic_arn = settings.SNS_TOPIC_ARN

    def send_notification(self, message, subject="Work Session Update"):
        """Function to send SNS notifications"""
        try:
            response = self.client.publish(
                TopicArn=self.topic_arn,
                Subject=subject,
                Message=message
            )
            print(f"✅ SNS Notification Sent: {response}")
            return response
        except ClientError as e:
            print(f"❌ Error sending SNS message: {e}")
            return None
