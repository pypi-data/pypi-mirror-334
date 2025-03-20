# Make this directory recognized as a Python package (__init__.py)

"""library functionality"""

from time_tracker.utils.cloudwatch_log import (
    create_log_group_and_stream,
    write_to_cloudwatch_log,
    log_login_sucess_failure_attempt,
)
from time_tracker.utils.DynamoDB import (
    save_user_to_dynamodb,
    update_user_picture,
    save_worktime_to_dynamodb,
    save_project_to_dynamodb,
)
from time_tracker.utils.notifications import SNSNotification
from time_tracker.utils.s3_storage import S3Storage
from time_tracker.utils.sqs_helper import (
    send_message_to_sqs,
    receive_message_from_sqs,
)