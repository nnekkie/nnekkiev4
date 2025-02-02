import boto3
from botocore.client import Config
from django.conf import settings



def generat_presigned_url(filepath, location='protected'):
    object_storage_key = f"{location}/{filepath}"
    s3 = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        aws_s3_custom_domain=settings.AWS_S3_CUSTOM_DOMAIN,
        config=Config(signature_version=settings.AWS_S3_SIGNATURE_VERSION)

    )
    url = s3.generate_presigned_url(
        ClientMethod="get_object",
        Params ={
            "Bucket":settings.AWS_STORAGE_BUCKET_NAME,
            "key":object_storage_key,
            "ResponseContentDisposition":"attachment",

        },
        ExpiresIn=3600,
    )
    return url
