
# OpenAI Whisper Lambda Function
## Overview
This repository contains Lambda functions designed to facilitate the processing of media files, specifically for YouTube videos and web uploads. The functions are integrated with AWS services such as SQS (Simple Queue Service), S3 (Simple Storage Service), and Pusher for real-time updates. This README provides an overview of each Lambda function and instructions for usage.
## Functions
- `QuickTranslatesYoutubeAPI/lambda_function.py`: Processes which YouTube video to download.
- `QuickTranslatesYoutubeWorkerAPI/lambda_function.py`: Handles YouTube video download process.
- `QuickTranslatesWebAPI/lambda_function.py`: Handles web uploads of media files.
## Prerequisites

Before using the Lambda functions, ensure you have the following prerequisites:

- AWS account with necessary permissions and credentials configured.
- Python environment set up with required dependencies (specified in requirements.txt).
- Configuration parameters set up (e.g., AWS_REGION_NAME, PUSHER_APP_ID, etc.).
## Setup Instructions
- Clone this repository to your local machine.
- Make a directory called python and install dependencies for lambda layers by running:
    ```bash
    cd python && pip install <package-name> -t .
    ```
- Configure environment variables or update config.py with necessary parameters.
- Zip `lambda_function.py` and `config.py`. Deploy the zip to AWS Lambda.
- Set up SQS queues and S3 buckets as per the configuration.
- Ensure Pusher credentials are configured for real-time updates.
## Usage
### QuickTranslatesYoutubeAPI/lambda_function.py
This function is designed to handle HTTP requests. It gathers metadata for YouTube video specified by its URL.

### QuickTranslatesYoutubeWorkerAPI/lambda_function.py
This function is triggered by messages from an SQS queue (specified by YOUTUBE_QUEUE_URL). It downloads a YouTube video specified by its URL, uploads it to an S3 bucket, and sends a message to another SQS queue (WORKER_QUEUE_URL) for further processing.

### QuickTranslatesWebAPI/lambda_function.py
This function is designed to handle HTTP requests. It expects a JSON payload containing the file_uri, language, and sub_language parameters. It then sends a message to the specified SQS queue (WORKER_QUEUE_URL) for processing.
## Authors

- [@farankhalid](https://www.github.com/farankhalid)
- [@aromabear](https://github.com/aromabear)
- [@Tabed23](https://github.com/Tabed23)
