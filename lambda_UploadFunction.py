import json
import boto3
import base64

s3 = boto3.client('s3')
BUCKET_NAME = 'aws-lambda-file-server-bucket'  

def lambda_handler(event, context):
    try:
        # Get filename from query string
        file_name = event['queryStringParameters']['fileName']

        # API Gateway sends binary as base64
        file_content = base64.b64decode(event["body"])

        # Upload to S3
        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=file_name,
            Body=file_content
        )

        return {
            "statusCode": 200,
            "body": json.dumps("File uploaded successfully")
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps("Error uploading file: " + str(e))
        }
