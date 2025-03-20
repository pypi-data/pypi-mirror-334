import uuid
import boto3
from django.conf import settings
from botocore.exceptions import ClientError

s3 = boto3.client('s3', region_name='us-east-1')

class S3Storage:
    """S3 Storage Handler"""

    def __init__(self):
        self.s3 = boto3.client('s3', region_name='us-east-1')
        self.bucket_name = settings.AWS_STORAGE_BUCKET_NAME
        self.ensure_bucket_exists()  # if thers is no bucket > create bucket

    def ensure_bucket_exists(self):
        """Check if the S3 bucket exists, and create if it does not exist."""
        try:
            self.s3.head_bucket(Bucket=self.bucket_name)
            print(f"======> Bucket '{self.bucket_name}' already exists.")
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == '404':
                print(f"XXXXXXXX>>> Bucket '{self.bucket_name}' does not exist. Creating...")
                self.create_bucket()
            elif error_code == '403':
                print(f" OOOOOOO >>> Bucket '{self.bucket_name}' exists but access is denied!")
            else:
                print(f" Error checking bucket: {e}")

    def create_bucket(self):
        """Create an S3 bucket if it does not exist."""
        try:
            self.s3.create_bucket(
                Bucket=self.bucket_name,
                CreateBucketConfiguration={'LocationConstraint': 'us-east-1'}
            )
            print(f"👹👹👹👹👹 Bucket '{self.bucket_name}' created successfully.")
        except ClientError as e:
            print(f"😸😸😸😸😸 Error creating bucket: {e}")

    def upload_file(self, file, folder="profile_pictures"):
        """
        Upload a file to S3 and return the file URL.
        :param file: File to upload (InMemoryUploadedFile)
        :param folder: Folder in the bucket (default is profile_pictures)
        :return: File URL stored in S3
        """
        # Extract file extension
        file_extension = file.name.split('.')[-1]
        # Create a unique file name (e.g., profile_pictures/uuid4.jpg)
        unique_filename = f"{folder}/{uuid.uuid4()}.{file_extension}"
        
        # Upload file with public read access
        self.s3.upload_fileobj(
            file,
            self.bucket_name,
            unique_filename,
            ExtraArgs={
                'ContentDisposition': 'inline',
                'ContentType': file.content_type
            }
        )
        
        # Return the file URL
        file_url = f"https://{settings.AWS_S3_CUSTOM_DOMAIN}/{unique_filename}"
        return file_url