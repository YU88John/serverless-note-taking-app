import os
import boto3
import json

def lambda_handler(event, context):
    bucket_name = os.environ.get('S3_BUCKET_NAME')

    if not bucket_name:
        return {
            'statusCode': 400,
            'body': json.dumps({'S3_BUCKET_NAME environment variable not set'})
        }

    # Create an S3 client
    s3 = boto3.client('s3')

    objects = s3.list_objects_v2(Bucket=bucket_name)
    if 'Contents' in objects:
        for obj in objects['Contents']:
            s3.delete_object(Bucket=bucket_name, Key=obj['Key'])
    
    return {
        'statusCode': 200,
        'body': json.dumps({'All objects deleted from S3 bucket': bucket_name})
    }
