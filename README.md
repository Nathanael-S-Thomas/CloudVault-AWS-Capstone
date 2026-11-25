# CloudVault – Secure Cloud-Based File Storage & Management

CloudVault is a Flask web app for uploading, listing, downloading and deleting files. It runs locally with filesystem storage and switches to Amazon S3 when `AWS_BUCKET_NAME` is configured.

## Features
- Clean responsive dashboard
- Upload, list, download and delete files
- Local mode for development, S3 mode for AWS
- S3 downloads use temporary presigned URLs
- Health endpoint (`/health`)
- 25 MB upload limit and file-extension allowlist

## Run locally
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```
Visit http://127.0.0.1:5000. Local files are saved in `uploads/`.

## Enable Amazon S3
1. Create a private S3 bucket in your chosen region.
2. Configure an EC2 instance role with least-privilege access to that bucket (recommended; avoid embedding access keys).
3. Set `AWS_BUCKET_NAME` and `AWS_REGION` in the environment.
4. Restart the application. It automatically switches to S3 storage.

Example:
```bash
export AWS_BUCKET_NAME=your-unique-bucket-name
export AWS_REGION=ap-south-1
python app.py
```

## AWS capstone service plan
- **EC2** – runs Flask
- **S3** – stores user files
- **IAM** – EC2 role for controlled S3 access
- **EBS** – EC2 root/data volume
- **VPC** – public/private networking and security groups
- **ELB (ALB)** – routes HTTP traffic to instances
- **Auto Scaling** – maintains EC2 capacity

> ALB and Auto Scaling are infrastructure components to configure separately; the starter app alone does not provision them. For a class demo, show each component configured and test the app through the ALB.

## Suggested demo
1. Open CloudVault dashboard.
2. Upload a file.
3. Show the file listed.
4. Download and delete it.
5. Demonstrate `/health`.
6. Show S3 bucket object, EC2 instance, IAM role, VPC, EBS, ALB and Auto Scaling in AWS Console.

## Security reminders
- Keep the S3 bucket private.
- Use an IAM instance role instead of access keys on EC2.
- Configure security groups narrowly; do not expose SSH to everyone if avoidable.
- Change `FLASK_SECRET_KEY` and consider HTTPS, authentication, CSRF protection and a database before production use.

## Team
Add your team members' names and roll numbers here.
