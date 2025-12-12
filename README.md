# Serverless File Sharing Platform – Step-by-Step Guide
Serverless file server using AWS Lambda + API Gateway (Free Tier)

## Overview
This project demonstrates how to build a **serverless file sharing system** using AWS services.  
It enables users to upload and download files securely through a lightweight HTTP interface.  
The solution combines **Amazon S3** for storage, **AWS Lambda** for compute, and **API Gateway** for API management which ensures scalability, durability, and simplicity.

---

## Key Features
- **Secure Uploads**: Store files directly in S3 with controlled access.  
- **Easy Downloads**: Retrieve files via simple GET requests.  
- **Scalable Architecture**: Serverless design that grows automatically with demand.  
- **Minimal Frontend**: A clean HTML interface for file server.  

---

## Architecture
The platform consists of three main components:
1. **Amazon S3** → Stores uploaded files.  
2. **AWS Lambda** → Handles upload and download logic.  
3. **API Gateway** → Provides REST endpoints for client interaction.  

![Architecture Diagram](docs/Architecture.png)

---

## Prerequisites
- An AWS account with permissions for S3, Lambda, and API Gateway.  
- Basic knowledge of AWS CLI or Console.  

## Steps to Deploy

### Step 1: S3 Bucket Creation
- Create an Amazon S3 bucket for file storage.
- Configure bucket name and region.
  - Bucket Name: `aws-lambda-file-server-bucket`
- Apply basic bucket policies for access control.

### Step 2: Create Lambda Functions

#### Upload Function
- **Name:** `UploadFunction`
- **Runtime:** Python 3.9
- **Role:** IAM role with `s3:PutObject` permission
- **Code:** Use the UploadFunction Python code.
- **Responsibility:** Accepts file content from API Gateway and writes it to S3.

#### Download Function
- **Name:** `DownloadFunction`
- **Runtime:** Python 3.9
- **Role:** IAM role with `s3:GetObject` permission
- **Code:** Use the DownloadFunction Python code.
- **Responsibility:** Fetches file from S3 and returns it to the client.

---

### Step 3: Configure API Gateway
- **API Name:** `file-sharing-api-amc`
- **Resource Path:** `/files`
- **Methods:**
  - `POST` → integrates with `UploadFunction`
  - `GET` → integrates with `DownloadFunction`
  - `OPTIONS` → for CORS preflight
- **Enable CORS:** Allow `GET`, `POST`, and `OPTIONS` from browsers.
- **Binary Media Types:** (API Gateway → Settings)
Add the following media types to support text, binary, and image uploads:
```
  */*   
  application/octet-stream  
  image/jpeg  
  image/png  
  application/pdf  
  application/vnd.openxmlformats-officedocument.wordprocessingml.document   
  multipart/form-data  
  image/*  
```
---

### Step 4: Method Configuration
For POST and GET methods, configure Lambda integration with UploadFunction and DownloadFunction respectively.

#### POST Method
- **Purpose:** Handle file uploads via `UploadFunction`.
- **Integration Request:**
  - Enable Lambda Proxy Integration. No mapping templates are required as the Lambda receives the full request context.

#### GET Method
- **Purpose:** Retrieve files from S3 via `DownloadFunction`.
- **Integration Request:**
  - Enable Lambda Proxy Integration. No mapping templates are required as the Lambda receives the full request context.
  
---

### Step 5: Deploy the API
- In API Gateway, click **Actions → Deploy API**.
- Select the stage (e.g., `dev`).
- After deployment, note the **Invoke URL**:

---

### Step 6: Testing the File Upload and Download
Once your API Gateway and Lambda integration is deployed, you can test the functionality by uploading and downloading files. You can use either **Postman** or the **cURL utility**.

  ***i. Upload a File***

#### Using Postman:
1. Open Postman and create a new request.  
2. Set the **method** to `POST`.  
3. Enter the URL in the format: `https://<api-id>.execute-api.<region>.amazonaws.com/dev/files?fileName=test.txtfileName=testing.txt`
4. In the **Headers**, set:  
- Content-Type: text/plain
5. In the **Body**, select **raw** and enter the file content.
6. Send the request. The file will be uploaded to your S3 bucket.

#### Using cURL:
```bash
curl --location 'https://<api-id>.execute-api.<region>.amazonaws.com/dev/files?fileName=hello.txt' \
--form 'file=@"/C:/Users/hp/Desktop/hello.txt"'
```

  ***ii. Download a File***
You can verify that the file was uploaded correctly by downloading it back from the API.

#### Using Postman:
1. Open Postman and create a new request.  
2. Set the **method** to `GET`.  
3. Enter the URL in the format: `https://<api-id>.execute-api.<region>.amazonaws.com/dev/files?fileName=test.txt`
4. Send the request.  
5. The response should return the file content you uploaded (e.g., `Hello World!`).

#### Using cURL:
```bash
curl --location 'https://<api-id>.execute-api.<region>.amazonaws.com/dev/files?fileName=hello.txt'
```

---

### Step 7: Frontend Deployment (Optional)
You can host a simple HTML/JavaScript frontend on **Amazon S3** to interact with your API Gateway + Lambda file server.

#### 1. Create S3 Bucket
- Go to **AWS Console → S3 → Create bucket**.
- Choose a unique name (e.g., `file-server-frontend-bucket`) and same region as your API.
- Enable **Static website hosting** in bucket **Properties**.
- Set **Index document** to `index.html`.

#### 2. Upload Frontend Files
- Upload your `index.html` (and any CSS/JS files).
- Make objects publicly readable (bucket policy or object permissions).
- Bucket policy for public read:
  ```json
  {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AllowPublicRead",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::file-server-frontend-bucket/*"
        }
    ]
  }

#### 3. API Integration for Frontend
Make sure your API Gateway is configured correctly before testing the frontend.

### Method Response Headers

#### For `GET /files`
- Status: `200`
- Response headers:
  - `Access-Control-Allow-Origin`
  - `Content-Disposition`
  - `Content-Type`

#### For `POST /files`
- Status: `200`
- Response headers:
  - `Access-Control-Allow-Origin`

#### For `OPTIONS /files`
- Status: `200`
- Response headers:
  - `Access-Control-Allow-Headers`
  - `Access-Control-Allow-Methods`
  - `Access-Control-Allow-Origin`

#### Integration Response Headers (OPTIONS → 200)
Map the following headers:
```text
method.response.header.Access-Control-Allow-Headers: 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'
method.response.header.Access-Control-Allow-Methods: 'GET,OPTIONS,POST'
method.response.header.Access-Control-Allow-Origin: '*'
```

#### 4. Connect Frontend to API
- In your `index.html`, set the API base URL:
  ```javascript
  const API_BASE = "https://<api-id>.execute-api.<region>.amazonaws.com/dev/files";

- Replace `<api-id>` and `<region>` with your actual API Gateway values.
- The frontend will use this base URL to send:
  - **POST** requests for file uploads.
  - **GET** requests for file downloads.

#### 5. Test Frontend
- Open the **Static website hosting URL** (e.g., `http://<your-bucket-name>.s3-website-<region>.amazonaws.com`).
- Use the **Upload card** to select and send a file.
- Use the **Get Files card** to list all available files stored in S3.
- Then use the **Download card** to download a specific file (e.g., `test.txt`) and verify that the correct content is returned.

#### 6. Troubleshooting:
- Common errors:
- {"message":"Missing Authentication Token"} → wrong path or method.
- CORS errors → missing OPTIONS headers.
- 403 Forbidden → bucket policy not set.
---
