import json
import boto3
import base64

s3 = boto3.client('s3')
BUCKET_NAME = 'aws-lambda-file-server-bucket' # Replace with your actual bucket name


def lambda_handler(event, context):
    try:
        query_params = event.get('queryStringParameters')

        # If fileName is provided → Download the file
        if query_params and query_params.get('fileName'):
            file_name = query_params['fileName']
            print(f"Downloading file: {file_name}")

            # CRITICAL FIX 1: Fetch metadata to get ContentType 
            head_obj = s3.head_object(Bucket=BUCKET_NAME, Key=file_name)
            s3_content_type = head_obj.get('ContentType', 'application/octet-stream')

            file_obj = s3.get_object(Bucket=BUCKET_NAME, Key=file_name)
            file_content = file_obj['Body'].read()

            print(f"S3 Content-Type found: {s3_content_type}")
            
            # Determine if it should be treated as text content
            is_text_content = s3_content_type.startswith('text/') or 'application/json' in s3_content_type

            if is_text_content:
                # Return text data as RAW (isBase64Encoded: False)
                try:
                    body = file_content.decode('utf-8')
                    
                    return {
                        "statusCode": 200,
                        "isBase64Encoded": False, 
                        "body": body,
                        "headers": {
                            # CRITICAL FIX 2: Use the actual S3 Content-Type
                            "Content-Type": s3_content_type, 
                            "Content-Disposition": f'attachment; filename="{file_name}"',
                            "Access-Control-Allow-Origin": "*",
                            "Access-Control-Allow-Headers": "*",
                            "Access-Control-Allow-Methods": "GET, OPTIONS"
                        }
                    }

                except UnicodeDecodeError:
                    # Fall through to binary handling if text decoding fails
                    pass 

            # Handle Binary Files (or failed text decode)
            print("Treating as binary file: Base64 encoding body.")
            body = base64.b64encode(file_content).decode('utf-8')

            # CRITICAL FIX 3: Return binary data as Base64 (isBase64Encoded: True)
            return {
                "statusCode": 200,
                "isBase64Encoded": True, 
                "body": body,
                "headers": {
                    # CRITICAL FIX 4: Use the actual S3 Content-Type
                    "Content-Type": s3_content_type, 
                    "Content-Disposition": f'attachment; filename="{file_name}"',
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Headers": "*",
                    "Access-Control-Allow-Methods": "GET, OPTIONS"
                }
            }

        # Otherwise → List all files
        else:
            print("Listing all files")
            response = s3.list_objects_v2(Bucket=BUCKET_NAME)

            files = [obj['Key'] for obj in response.get('Contents', [])]

            return {
                "statusCode": 200,
                "headers": {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Headers": "*",
                    "Access-Control-Allow-Methods": "GET, OPTIONS",
                    "Content-Type": "application/json"
                },
                "body": json.dumps(files)
            }

    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()

        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Methods": "GET, POST, OPTIONS"
            },
            "body": json.dumps({"error": str(e)})
        }
