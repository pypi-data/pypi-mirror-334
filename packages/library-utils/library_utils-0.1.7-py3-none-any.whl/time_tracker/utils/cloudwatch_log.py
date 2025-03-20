import uuid
import time
import boto3
from botocore.exceptions import ClientError
from django.http import HttpResponse

# create CloudWatch client
client = boto3.client('logs', region_name='us-east-1')

#Automatically detect IAM roles
session = boto3.Session()

log_group_name = 'WorkSessionLogs'
log_stream_name = 'WorkSessionStream'

def create_log_group_and_stream():
    """ create log group and stream in cloudwatch """
    try:
        response = client.describe_log_groups(logGroupNamePrefix=log_group_name)
        if not any(group['logGroupName'] == log_group_name for group in response.get('logGroups', [])):
            client.create_log_group(logGroupName=log_group_name)
            print(f"Created log group: {log_group_name}")
    except ClientError as e:
        print(f"Error creating log group: {e}")

    try:
        response = client.describe_log_streams(
            logGroupName=log_group_name,
            logStreamNamePrefix=log_stream_name
        )
        if not any(stream['logStreamName'] == log_stream_name for stream in response.get('logStreams', [])):
            client.create_log_stream(
                logGroupName=log_group_name,
                logStreamName=log_stream_name
            )
            print(f"Created log stream: {log_stream_name}")
    except ClientError as e:
        print(f"Error creating log stream: {e}")

def write_to_cloudwatch_log(message):
    """when user uses application 
    cloudwactch can write to log"""
    timestamp = int(round(time.time() * 1000))  # Generate a timestamp in milliseconds

    try:
        response = client.describe_log_streams(
            logGroupName=log_group_name,
            logStreamNamePrefix=log_stream_name
        )

        # create if there is no stream
        if not response['logStreams']:
            client.create_log_stream(
                logGroupName=log_group_name,
                logStreamName=log_stream_name
            )

        # log record
        response = client.put_log_events(
            logGroupName=log_group_name,
            logStreamName=log_stream_name,
            logEvents=[
                {
                    'timestamp': timestamp,
                    'message': message
                }
            ]
        )
        print(f"Log successfully written to CloudWatch: {message}")
    except ClientError as e:
        print(f"Error writing log to CloudWatch: {e}")

# 서버 시작 시 한 번만 로그 그룹과 스트림을 생성
create_log_group_and_stream()