import boto3
from botocore.exceptions import ClientError
from config import Config
class s3Storage:
    def __init__(self):
        self.s3=boto3.client(
            's3',
            aws_access_key_id
        )