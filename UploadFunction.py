import json
import boto3
import base64
from io import BytesIO
from email import message_from_bytes

s3 = boto3.client('s3')
BUCKET_NAME = 'aws-lambda-file-server-bucket'  # Replace with your actual bucket name


def lambda_handler(event, context):
    try:
        # Validate fileName parameter
        query_params = event.get('queryStringParameters', {})
        if not query_params or not query_params.get('fileName'):
            return {
                "statusCode": 400,
                "headers": {"Access-Control-Allow-Origin": "*"},
                "body": json.dumps({"error": "Missing fileName parameter"})
            }

        file_name = query_params['fileName']
        
        # Get request body and headers
        body = event.get("body", "")
        is_base64 = event.get('isBase64Encoded', False)
        headers = event.get('headers', {})
        
        # Get Content-Type header (case-insensitive)
        content_type_header = headers.get('Content-Type') or headers.get('content-type', '')
        
        print(f"Uploading file: {file_name}")
        print(f"Content-Type header: {content_type_header}")
        print(f"Is Base64 Encoded: {is_base64}")

        # Decode base64 body if needed
        if is_base64:
            body_bytes = base64.b64decode(body)
        else:
            body_bytes = body.encode('utf-8') if isinstance(body, str) else body

        # Parse multipart/form-data
        if 'multipart/form-data' not in content_type_header:
            raise ValueError("Expected multipart/form-data content type")

        # Parse the multipart data using email library
        # Add Content-Type header to the body for proper parsing
        message_bytes = f"Content-Type: {content_type_header}\r\n\r\n".encode() + body_bytes
        message = message_from_bytes(message_bytes)
        
        file_content = None
        content_type = 'application/octet-stream'
        
        # Extract file from multipart message
        for part in message.walk():
            if part.get_content_disposition() == 'form-data':
                # Check if this part has a filename (it's a file upload)
                content_disposition = part.get('Content-Disposition', '')
                if 'filename=' in content_disposition:
                    file_content = part.get_payload(decode=True)
                    content_type = part.get_content_type() or 'application/octet-stream'
                    print(f"Extracted file type: {content_type}")
                    break

        if file_content is None:
            raise ValueError("Could not extract file from multipart form. Ensure form field name is 'file'")

        print(f"File content length: {len(file_content)} bytes")

        # Upload to S3 with correct Content-Type
        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=file_name,
            Body=file_content,
            ContentType=content_type
        )

        print(f"Successfully uploaded {file_name} to S3")

        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Methods": "POST, OPTIONS",
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "message": "File uploaded successfully",
                "fileName": file_name,
                "size": len(file_content),
                "contentType": content_type
            })
        }

    except Exception as e:
        print(f"Upload error: {str(e)}")
        import traceback
        traceback.print_exc()

        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Methods": "POST, OPTIONS",
                "Content-Type": "application/json"
            },
            "body": json.dumps({"error": str(e)})
        }
