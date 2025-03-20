import uuid
import boto3
from django.conf import settings

s3 = boto3.client('s3', region_name='us-east-1')

class S3Storage:
    """create s3 bucket"""
    def __init__(self):
        self.s3 = boto3.client(
            's3',
            region_name='us-east-1'
        )
        self.bucket_name = settings.AWS_STORAGE_BUCKET_NAME

    def upload_file(self, file, folder="profile_pictures"):
        """
        Upload a file to S3 and return the file URL.
        :param file: File to upload (InMemoryUploadedFile)
        :param folder: Folder in the bucket (default is profile_pictures)
        :return: File URL stored in S3
        """
        # Extract file extension
        file_extension = file.name.split('.')[-1]
        # Create a unique file name (e.g. profile_pictures/uuid4.jpg)
        unique_filename = f"{folder}/{uuid.uuid4()}.{file_extension}"
         # Set public read permissions and Content-Disposition to inline when uploading via ExtraArgs.
        self.s3.upload_fileobj(
            file,
            self.bucket_name,
            unique_filename,
            ExtraArgs={
                'ContentDisposition': 'inline',
                'ContentType': file.content_type
            }
        )
        file_url = f"https://{settings.AWS_S3_CUSTOM_DOMAIN}/{unique_filename}"
        return file_url
