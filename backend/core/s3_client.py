# core/s3_client.py

import boto3
import os
from typing import List

class S3FileManager:
    def __init__(self, bucket_name: str, base_path: str = ""):
        self.bucket_name = bucket_name
        self.base_path = base_path
        self.s3 = boto3.client(
            "s3",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=os.getenv("AWS_REGION", "us-east-1")
        )

    def list_files(self) -> List[str]:
        response = self.s3.list_objects_v2(Bucket=self.bucket_name, Prefix=self.base_path)
        files = [content['Key'] for content in response.get('Contents', [])]
        return files

    def load_s3_pdf(self, key: str) -> bytes:
        obj = self.s3.get_object(Bucket=self.bucket_name, Key=key)
        return obj['Body'].read()

    def upload_file(self, file_path: str, key: str) -> None:
        self.s3.upload_file(file_path, self.bucket_name, key)