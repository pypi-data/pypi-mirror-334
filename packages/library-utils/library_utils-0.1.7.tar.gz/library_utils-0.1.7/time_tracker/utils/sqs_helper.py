import boto3
from botocore.exceptions import ClientError
from django.conf import settings

sqs = boto3.client('sqs', region_name='us-east-1')

def send_message_to_sqs(message_body):
    """Sending a message to an SQS queue"""
    try:
        response = sqs.send_message(
            QueueUrl=settings.SQS_QUEUE_URL,
            MessageBody=message_body
        )
        print(f"Message sent to SQS: {response['MessageId']}")
    except ClientError as e:
        print(f"Error sending message to SQS: {e}")

def receive_message_from_sqs():
    """Receiving messages from an SQS queue"""
    try:
        # 메시지 수신
        response = sqs.receive_message(
            QueueUrl=settings.SQS_QUEUE_URL,
            MaxNumberOfMessages=1,  # Receive up to 1 message
            WaitTimeSeconds=10  # Long Polling (10초 대기)
        )

        messages = response.get('Messages', [])
        if not messages:
            print("No messages in the queue.")
            return None

        # Get the first message
        message = messages[0]
        receipt_handle = message['ReceiptHandle']

        # Delete message (received message should be deleted from SQS)
        sqs.delete_message(
            QueueUrl=settings.SQS_QUEUE_URL,
            ReceiptHandle=receipt_handle
        )

        print(f"Message received from SQS: {message['Body']}")
        return message['Body']

    except ClientError as e:
        print(f"Error receiving message from SQS: {e}")
        return None
