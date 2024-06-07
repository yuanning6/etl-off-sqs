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
    git clone <repository-url>
    cd <repository-name>
    ```

2. Create and activate a virtual environment:

    ```sh
    python -m venv venv
    ```

    - On Windows:
        ```sh
        .\venv\Scripts\activate
        ```
    - On macOS/Linux:
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

### Running the Application

1. Run the ETL script:

    ```sh
    python main.py
    ```

### Explanation of PII Masking and Version Conversion

#### PII Masking

To keep personal identifiable information (PII) safe while still being able to spot duplicate values, `mask_pii` function uses a consistent hashing method. It applies the `SHA-256` hashing algorithm to mask the `device_id` and `ip` fields. This means that the same input value will always produce the same hashed output, making it easy to identify duplicates without exposing the actual data.

#### Version String Conversion

The `version_to_int` function handles different version formats by ensuring the version string is always processed into three parts: major, minor, and patch. It splits the version string and pads it with zeros if necessary to ensure there are always three components. It then combines these components into a single integer for storage in the database.

### Questions




### Future Improvements

- Implement error handling and logging.
- Add unit and integration tests.
- Enable configuration via environment variables.
- Add more robust masking techniques for PII data.
