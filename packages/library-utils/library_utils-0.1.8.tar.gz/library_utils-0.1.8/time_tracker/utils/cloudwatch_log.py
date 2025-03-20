import uuid
import time
import boto3
from botocore.exceptions import ClientError
from django.http import HttpResponse

# create CloudWatch client
client = boto3.client('logs', region_name='us-east-1')

#Automatically detect IAM roles
session = boto3.Session()

# check work start and end/end_anyway
log_group_name = 'WorkSessionLogs'
log_stream_name = 'WorkSessionStream'

# login event log
login_log_group = 'LoginAttemptLogs'
login_log_stream = 'LoginEventsStream'

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
   
    # login event - log group and stream
    try:
        response = client.describe_log_groups(logGroupNamePrefix=login_log_group)
        if not any(group['logGroupName'] == login_log_group for group in response.get('logGroups', [])):
            client.create_log_group(logGroupName=login_log_group)
            print(f"Created login log group: {login_log_group}")
    except ClientError as e:
        print(f"Error creating login log group: {e}")

    try:
        response = client.describe_log_streams(
            logGroupName=login_log_group,
            logStreamNamePrefix=login_log_stream
        )
        if not any(stream['logStreamName'] == login_log_stream for stream in response.get('logStreams', [])):
            client.create_log_stream(
                logGroupName=login_log_group,
                logStreamName=login_log_stream
            )
            print(f"Created login log stream: {login_log_stream}")
    except ClientError as e:
        print(f"Error creating login log stream: {e}")


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

# login suceess or failure function
def log_login_sucess_failure_attempt(username, status, ip_address):
    """ Logs login attempts to CloudWatch (Success/Failure) """
    timestamp = int(round(time.time() * 1000))
    message = f"Login attempt | User: {username} | Status: {status} | IP: {ip_address} | Timestamp: {timestamp}"

    try:
        response = client.put_log_events(
            logGroupName=login_log_group,
            logStreamName=login_log_stream,
            logEvents=[
                {
                    'timestamp': timestamp,
                    'message': message
                }
            ]
        )
        print(f"Login event logged: {message}")
    except ClientError as e:
        print(f"Error logging login event: {e}")

# 서버 시작 시 한 번만 로그 그룹과 스트림을 생성
create_log_group_and_stream()