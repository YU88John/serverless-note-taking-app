import json
import os
import boto3
from botocore.exceptions import ClientError

# Get the DynamoDB table name and S3 bucket name from environment variables
table_name = os.environ.get('DYNAMODB_TABLE_NAME')
s3_bucket_name = os.environ.get('S3_BUCKET_NAME')

# Create DynamoDB and S3 resources with aws sdk
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(table_name)
s3 = boto3.client('s3')

def lambda_handler(event, context):
    # Extract values directly from the query string parameters
    created_at = event.get('queryStringParameters', {}).get('CreatedAt')
    name = event.get('queryStringParameters', {}).get('Name')

    try:
        # Retrieve metadata from DynamoDB
        response = table.get_item(
            Key={
                'CreatedAt': created_at,
                'Name': name
            }
        )

        # Check if the item was found
        if 'Item' in response:
            item = response['Item']

            # Fetch note content from S3
            s3_object_key = f'notes/{name}.txt'  

            # Delete content from S3
            s3.delete_object(Bucket=s3_bucket_name, Key=s3_object_key)

            # Delete metadata from DynamoDB
            response = table.delete_item(
                Key={
                    'CreatedAt': created_at,
                    'Name': name
                }
            )

            return {
                'statusCode': 200,
                'body': json.dumps({'message': 'Item and associated content deleted successfully'})
            }
        else:
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'Item not found'})
            }

    except ClientError as e:
        error_message = str(e)
        print(f"Error: {error_message}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': error_message})
        }

    except Exception as e:
        error_message = str(e)
        print(f"Unexpected error: {error_message}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Internal Server Error'})
        }
