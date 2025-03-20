import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv
import os


load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv('VAIA_AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('VAIA_AWS_SECRET_ACCESS_KEY')
AWS_REGION = os.getenv('VAIA_AWS_REGION')

boto3.setup_default_session(
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)


def upload_bytes_to_s3(file_bytes: bytes, bucket: str, object_name: str) -> str:
    """
    Upload bytes directly to S3 without saving to disk
    """
    s3_client = boto3.client('s3')
    try:
        s3_client.put_object(
            Body=file_bytes,
            Bucket=bucket,
            Key=object_name,
            ContentType='image/jpeg'  
        )
        s3_url = f"https://{bucket}.s3.{AWS_REGION}.amazonaws.com/{object_name}"
        return s3_url
    except ClientError as e:
        print(f"Error uploading bytes to S3: {e}")
        return ""