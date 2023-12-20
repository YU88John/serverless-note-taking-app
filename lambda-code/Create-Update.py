import json
import os
import boto3
from botocore.exceptions import ClientError
from datetime import datetime
import uuid  # for generating unique NoteID

# Get the DynamoDB table name and S3 bucket name from environment variables
table_name = os.environ.get('DYNAMODB_TABLE_NAME')
s3_bucket_name = os.environ.get('S3_BUCKET_NAME')

# Create DynamoDB and S3 resources
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(table_name)
s3 = boto3.client('s3')

def lambda_handler(event, context):
    # Extract values directly from the event
    name = event.get('Name')
    content = event.get('Content')

    # Set date timestamp without time
    now = datetime.utcnow().date().isoformat()

    # Generate a unique NoteID
    note_id = str(uuid.uuid4())

    try:
        # Use the same S3 object key for updates
        s3_object_key = f'notes/{name}.txt'  # Use a meaningful object key based on the note name

        # Upload or overwrite content in S3
        s3.put_object(Body=content, Bucket=s3_bucket_name, Key=s3_object_key)

        # Update metadata in DynamoDB
        response = table.put_item(
            Item={
                'NoteID': note_id,
                'CreatedAt': now,
                'Name': name,
                'UpdatedAt': datetime.utcnow().isoformat(),
                # Add other metadata attributes as needed
            }
        )

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Note saved successfully'})
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