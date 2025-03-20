from datetime import datetime
import boto3
from botocore.exceptions import ClientError # delete

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

def create_tables():
    """create DynamoDB table"""
    try:
        dynamodb.create_table(
            TableName='Users',
            KeySchema=[
                {
                    'AttributeName': 'ID',
                    'KeyType': 'HASH'
                },
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'ID',
                    'AttributeType': 'S'
                },
            ],
            BillingMode='PAY_PER_REQUEST'
            # On-demand (Charge upon request)
        )
        print("Users table created successfully.")
    except ClientError as e:
        if 'ResourceInUseException' in str(e):
            print("Users table already exists.")
        else:
            print(f"Error creating Users table: {e}")
    try:
        dynamodb.create_table(
            TableName='Worktime',
            KeySchema=[
                {
                    'AttributeName': 'EntryID',
                    'KeyType': 'HASH'
                },
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'EntryID',
                    'AttributeType': 'S'
                }
            ],
            BillingMode='PAY_PER_REQUEST'
        )
        print("Worktime table created successfully.")
    except ClientError as e:
        if 'ResourceInUseException' in str(e):
            print("Worktime table already exists.")
        else:
            print(f"Error creating Worktime table: {e}")

    try:
        dynamodb.create_table(
            TableName='Projects',
            KeySchema=[
                {
                    'AttributeName': 'ProjectID',
                    'KeyType': 'HASH'
                },
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'ProjectID',
                    'AttributeType': 'S'
                },
            ],
            BillingMode='PAY_PER_REQUEST'
        )
        print("Projects table created successfully.")
    except ClientError as e:
        if 'ResourceInUseException' in str(e):
            print("Projects table already exists.")
        else:
            print(f"Error creating Projects table: {e}")
# Call to create table
create_tables()

def save_user_to_dynamodb(user_id, first_name, last_name, phone_number, email, picture):
    """Store users in DynamoDB when they sign up"""
    table = dynamodb.Table('Users')
    table.put_item(
        Item={
            'ID': user_id,
            'FirstName': first_name,
            'LastName': last_name,
            'PhoneNumber': phone_number,
            'Email': email,
            'Picture': picture  # URL
        }
    )
    print(f"User {first_name} {last_name} added to Users table.")

def update_user_picture(user_id, picture):
    """Update photo information in DynamoDB when updating profile photo"""
    table = dynamodb.Table('Users')
    try:
        # Convert ID to string and update
        table.update_item(
            Key={'ID': user_id},  # Set the ID field to user_id
            UpdateExpression="set Picture = :p",  # Update Picture field
            ExpressionAttributeValues={':p': picture}  # Value to store in Picture
        )
        print(f"User {user_id} profile picture updated.")
    except ClientError as e:
        print(f"Error updating profile picture for user {user_id}: {e}")

def save_worktime_to_dynamodb(entry_id, user_id, project_id, start_time, end_time, target_time, overtime):
    """Save data to Worktime table when work session ends"""
    # Make EntryID unique by combining it with user_id and timestamp
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    entry_id_str = f"{entry_id}-{timestamp}"

    # convert date to string
    start_time_str = start_time.strftime('%Y-%m-%d %H:%M:%S') if start_time else None
    end_time_str = end_time.strftime('%Y-%m-%d %H:%M:%S') if end_time else None

    # Check if there is an existing EntryID in DynamoDB
    table = dynamodb.Table('Worktime')
    response = table.get_item(Key={'EntryID': entry_id_str})

    # If EntryID does not exist, save it again
    if 'Item' not in response:
    # Calculate total working hours
    # (given start_time and end_time, calculate the difference between the two hours)
        total_work_time = None
        if start_time and end_time:
            duration = end_time - start_time
            total_seconds = duration.total_seconds()
            hours = int(total_seconds // 3600)
            minutes = int((total_seconds % 3600) // 60)
            total_work_time = f"{hours} hours {minutes} minutes"

        table = dynamodb.Table('Worktime')
        table.put_item(
            Item={
                'EntryID': entry_id_str,
                'UserID': entry_id_str,
                'ProjectID': project_id,
                'StartTime': start_time_str,
                'EndTime': end_time_str,
                'TargetTime': target_time,
                'Overtime': overtime,
                'TotalWorkTime': total_work_time
            }
        )
        print(f"Worktime entry {entry_id} added to Worktime table.")

def save_project_to_dynamodb(project_id, project_name, description):
    """Insert project information into the Projects table"""
    table = dynamodb.Table('Projects')
    try:
        #Convert project_id to a string and pass it
        project_id_str = str(project_id)
        print(f"Saving project{project_name} with ID {project_id_str} to DynamoDB")
        table.put_item(
            Item={
                'ProjectID': project_id,
                'ProjectName': project_name,
                'Description': description
            }
        )
        print(f"Project {project_name} added to Projects table.")
    except ClientError as e:
        print(f"Error saving project {project_name} to DynamoDB: {e}")

def delete_worktime_from_dynamodb(entry_id):
    """Delete Work Session function (delete specific work items from the Worktime table)"""
    table = dynamodb.Table('Worktime')

    try:
        response = table.delete_item(
            Key={'EntryID': str(entry_id)}
        )
        # Check deletion results
        if response.get('ResponseMetadata', {}).get('HTTPStatusCode') == 200:
            print(f"Worktime entry {entry_id} deleted successfully from Worktime table.")
            return True
        else:
            print(f"Failed to delete worktime entry {entry_id} from Worktime table.")
            return False

    except ClientError as e:
        print(f"Error deleting worktime entry {entry_id}: {e}")
        return False
