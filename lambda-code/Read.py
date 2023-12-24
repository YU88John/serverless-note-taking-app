import json
import os
import boto3
from botocore.exceptions import ClientError

# Get the DynamoDB table name and S3 bucket name from environment variables
table_name = os.environ.get('DYNAMODB_TABLE_NAME')
s3_bucket_name = os.environ.get('S3_BUCKET_NAME')

# Create DynamoDB and S3 resources
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(table_name)
s3 = boto3.client('s3')

def lambda_handler(event, context):
    # Extract values from query param
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
            s3_response = s3.get_object(Bucket=s3_bucket_name, Key=s3_object_key)
            note_content = s3_response['Body'].read().decode('utf-8')

            # Include note content in the response
            item['Content'] = note_content

            return {
                'statusCode': 200,
                'body': json.dumps({'message': 'Item found', 'item': item})
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




# Sample Lambda run query
    
# {
#  "queryStringParameters": {
#  "CreatedAt": "2023-12-21",
#   "Name": "SampleNameHola"
#  }
# }

