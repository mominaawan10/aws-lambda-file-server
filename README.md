# Serverless File Sharing Platform – Step-by-Step Guide
Serverless file server using AWS Lambda + API Gateway (Free Tier)

### Overview
This project demonstrates how to build a **serverless file sharing system** using AWS services.  
It enables users to upload and download files securely through a lightweight HTTP interface.  
The solution combines **Amazon S3** for storage, **AWS Lambda** for compute, and **API Gateway** for API management which ensures scalability, durability, and simplicity.

---

### Key Features
- **Secure Uploads**: Store files directly in S3 with controlled access.  
- **Easy Downloads**: Retrieve files via simple GET requests.  
- **Scalable Architecture**: Serverless design that grows automatically with demand.  
- **Minimal Frontend**: A clean HTML interface for file server.  

---

### Architecture
The platform consists of three main components:
1. **Amazon S3** → Stores uploaded files.  
2. **AWS Lambda** → Handles upload and download logic.  
3. **API Gateway** → Provides REST endpoints for client interaction.  

![Architecture Diagram](docs/Architecture.png)

---

### Prerequisites
- An AWS account with permissions for S3, Lambda, and API Gateway.  
- Basic knowledge of AWS CLI or Console.  

### Steps to Deploy

#### Step 1: S3 Bucket Creation
- Create an Amazon S3 bucket for file storage.
- Configure bucket name and region.
  - Bucket Name: `aws-lambda-file-server-bucket`
- Apply basic bucket policies for access control.

#### Step 2: Create Lambda Functions

### Upload Function
- **Name:** `UploadFunction`
- **Runtime:** Python 3.9
- **Role:** IAM role with `s3:PutObject` permission
- **Code:** Use the UploadFunction Python code.
- **Responsibility:** Accepts file content from API Gateway and writes it to S3.

### Download Function
- **Name:** `DownloadFunction`
- **Runtime:** Python 3.9
- **Role:** IAM role with `s3:GetObject` permission
- **Code:** Use the DownloadFunction Python code.
- **Responsibility:** Fetches file from S3 and returns it to the client.

---

#### Step 3: Configure API Gateway
- **API Name:** `file-sharing-api-amc`
- **Resource Path:** `/files`
- **Methods:**
  - `POST` → integrates with `UploadFunction`
  - `GET` → integrates with `DownloadFunction`
- **Enable CORS:** Allow `GET` and `POST` from browsers.

---

#### Step 4: Method Configuration

### GET Method
- **Purpose:** Retrieve files from S3 via `DownloadFunction`.
- **Setup:**
  - Validate query string parameter `fileName`.
  - Map incoming request to Lambda input using a JSON template.
  - 
- **Mapping Template Example:**
  ```json
  {
    "fileName": "$input.params('fileName')"
  }
  
---

#### Step 6: Configure POST Method
- **Purpose:** Handle file uploads via `UploadFunction`.
- **Integration Request:**
  - Go to **Integration Request → Mapping Templates**.
  - Add a new template with **Content Type:** `text/plain`.
  - Define the mapping to pass both file name and file content to Lambda.

- **Mapping Template Example:**
  ```json
  {
    "fileName": "$input.params('fileName')",
    "content": "$input.body"
  }
  
---

#### Step 7: Deploy API Gateway
- In API Gateway, click **Actions → Deploy API**.
- Select the stage (e.g., `dev`).
- After deployment, note the **Invoke URL**:
- https://csdg8czp44.execute-api.eu-north-1.amazonaws.com/dev

---

#### Step 8: Testing the File Upload and Download

Once your API Gateway and Lambda integration is deployed, you can test the functionality by uploading and downloading files. You can use either **Postman** or the **cURL utility**.

---

### Upload a File

## Using Postman
1. Open Postman and create a new request.  
2. Set the **method** to `POST`.  
3. Enter the URL in the format:  
- https://csdg8czp44.execute-api.eu-north-1.amazonaws.com/dev/files?fileName=test.txt
4. In the **Headers**, set:  
- Content-Type: text/plain
5. In the **Body**, select **raw** and enter the file content.
6. Send the request. The file will be uploaded to your S3 bucket.

Using cURL
```bash
curl --location 'https://<api-id>.execute-api.<region>.amazonaws.com/dev/files?fileName=test.txt' \
--header 'Content-Type: text/plain' \
--data 'Hello World from A Monk in Cloud!'

### Download a File

You can verify that the file was uploaded correctly by downloading it back from the API.

Using Postman
1. Open Postman and create a new request.  
2. Set the **method** to `GET`.  
3. Enter the URL in the format:  
- https://csdg8czp44.execute-api.eu-north-1.amazonaws.com/dev/files?fileName=test.txt

4. Send the request.  
5. The response should return the file content you uploaded (e.g., `Hello World!`).

### Using cURL
```bash
curl --location 'https://<api-id>.execute-api.<region>.amazonaws.com/dev/files?fileName=test.txt'

