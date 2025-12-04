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
#### 1. AWS Account Setup
- Create a new AWS account.
- Configure basic settings and security.


#### 2. IAM Users and Permissions
- Create IAM users for project access.
- Assign appropriate permissions.
- Ensure least‑privilege principle for security.

#### 3. S3 Bucket Creation
- Create an Amazon S3 bucket for file storage.
- Configure bucket name and region.
- Apply basic bucket policies for access control.
