# Data Engineering Take Home: ETL off a SQS Queue

## Overview

This application reads JSON data from an AWS SQS Queue, masks PII data, transforms the data, and writes it to a Postgres database. The entire setup runs locally using Docker.

## Setup

### Prerequisites

- Docker
- Docker Compose
- Python 3.9+
- pip
- awscli-local
- psql

### Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/yuanning6/etl-off-sqs.git
    cd etl-off-sqs
    ```

2. Create and activate a virtual environment:

    ```sh
    python -m venv venv

    or

    python3 -m venv venv (if using Python 3)
    ```

    - Activate on Windows:
        ```sh
        .\venv\Scripts\activate
        ```
    - Activate on macOS/Linux:
        ```sh
        source venv/bin/activate
        ```

3. Install Python dependencies:

    ```sh
    pip install -r requirements.txt
    ```

4. Start the Docker services:

    ```sh
    docker-compose up
    ```

    If encounter the error: Bind for 0.0.0.0:5432 failed: port is already allocated, stop the container running on port 5432.

## Running the Application

Run the ETL script:

    ```sh
    python main.py
    ```

## Explanation of PII Masking and Version String Conversion

### PII Masking

To keep personal identifiable information (PII) safe while still being able to spot duplicate values, `mask_pii` function uses a consistent hashing method. It applies the `SHA-256` hashing algorithm to mask the `device_id` and `ip` fields. This means that the same input value will always produce the same hashed output, making it easy to identify duplicates without exposing the actual data.

### Version String Conversion

The `version_to_int` function handles different version formats by ensuring the version string is always processed into three parts: major, minor, and patch. It splits the version string and pads it with zeros if necessary to ensure there are always three components. It then combines these components into a single integer for storage in the database.

The method is implemented using a bit masking technique from [here](https://softwareengineering.stackexchange.com/questions/313748/convert-version-string-to-integer):

1. Shift and Combine: The major, minor, and patch parts of the version are shifted and combined into a single integer.
2. Shift Left (<<) and OR (|): The major version is shifted left by 16 bits, the minor version by 8 bits, and the patch version is combined using the OR operator.

## Questions

### How would you deploy this application in production?

To deploy this application in production, I would use AWS services such as:

- **Amazon SQS** for queue management.
- **Amazon RDS** for the PostgreSQL database.
- **Amazon ECS** or Amazon EKS for container orchestration.
- **AWS Lambda** for serverless ETL processing, if appropriate.

I would also use CI/CD pipelines to automate the deployment process to ensure that code changes are tested and deployed efficiently.

### What other components would you want to add to make this production ready?

To make this application ready for production, I would add:

- Use **AWS CloudWatch** or a similar service for **monitoring and logging** to keep an eye on the application's health and log its activities.
- Add strong **error handling and retry mechanisms** to make sure messages from the queue are processed reliably.
- Encrypt data both in transit and at rest, use **AWS IAM** roles and policies to control access, and follow best practices for **security**.
- Set up **auto-scaling** for both the application and the database to handle more load as it comes in.
- Include thorough unit and integration **tests** to catch issues early and ensure everything works as expected.

### How can this application scale with a growing dataset?

The application can scale with a growing dataset by:

- Use **AWS ECS/EKS** to automatically scale the number of instances based on the load.
- Use **Amazon RDS with read replicas** and automated backups to manage a growing dataset.
- Implement **sharding or partitioning** strategies in the database to handle large volumes of data efficiently.
- Utilize the inherent scalability of Amazon SQS to handle an increasing number of messages.

### How can PII be recovered later on?

To recover PII later on, we would need to securely store the original PII data in a separate, encrypted database. The masked data should be linked to the original data in a way that allows for reverse lookup when necessary. Access to this data should be tightly controlled, with strict access policies and audit logging to track who accessed the data and when.

### What are the assumptions you made?

- The JSON messages in the SQS queue follow a consistent structure.
- The Localstack and Postgres services are correctly configured via Docker.
- The version strings in the data can be reliably converted to integers as described.

## Future Improvements

- Implement error handling and logging.
- Add unit and integration tests.
- Enable configuration via environment variables.
- Add more robust masking techniques for PII data.
