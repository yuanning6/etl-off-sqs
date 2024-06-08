import boto3
import hashlib
import psycopg2
import json
from datetime import datetime

# To fix the issue with the AWS SDK not being able to find the credentials
FAKE_AWS_SQS_CREDS = {
    "aws_access_key_id":"foobar",
    "aws_secret_access_key":"foobar"
}

# Configure AWS and PostgreSQL
sqs = boto3.client('sqs', endpoint_url="http://localhost:4566", **FAKE_AWS_SQS_CREDS)
queue_url = "http://localhost:4566/000000000000/login-queue"

conn = psycopg2.connect(
    dbname='postgres',
    user='postgres',
    password='postgres',
    host='localhost',
    port='5432'
)

# Function to mask PII data
def mask_pii(data):
    return hashlib.sha256(data.encode()).hexdigest()

# Convert version string to integer
def version_to_int(version):
    max_bits=8
    versions = [int(part) for part in version.split('.')] + [0] * (3 - len(version.split('.')))
    
    major = versions[0]
    minor = versions[1]
    patch = versions[2]
    
    return (major << (max_bits * 2)) | (minor << max_bits) | patch

# Function to process and insert message into Postgres
def process_message(message):
    data = json.loads(message['Body'])
    print("Received message data:", data)
    user_id = data['user_id']
    device_type = data['device_type']
    masked_ip = mask_pii(data['ip'])
    masked_device_id = mask_pii(data['device_id'])
    locale = data['locale']
    app_version = version_to_int(data['app_version'])
    create_date = datetime.now()

    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO user_logins (user_id, device_type, masked_ip, masked_device_id, locale, app_version, create_date)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    ''', (user_id, device_type, masked_ip, masked_device_id, locale, app_version, create_date))
    conn.commit()

# Read messages from SQS and process
def read_and_process_messages():
    response = sqs.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=10,
        WaitTimeSeconds=10
    )

    for message in response.get('Messages', []):
        process_message(message)

if __name__ == '__main__':
    read_and_process_messages()
