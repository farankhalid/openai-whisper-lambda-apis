import json
import boto3
import os
from pytube import YouTube
from pusher import Pusher
from config import (
    get_parameter,
    AWS_REGION_NAME,
    PUSHER_APP_ID,
    PUSHER_KEY,
    PUSHER_SECRET,
    PUSHER_CLUSTER,
    WORKER_QUEUE_URL,
    YOUTUBE_QUEUE_URL,
)


def download_youtube_video(video_url, download_path, job_id):
    try:
        yt = YouTube(video_url)
        stream = yt.streams.get_lowest_resolution()
        stream.download(output_path=download_path, filename=job_id)
        print(f"Downloaded to lambda path {download_path}")
        return True
    except Exception as e:
        print("Error:", str(e))
        return False


def upload_file_to_s3(file_path, bucket_name, s3_key):
    s3_client = boto3.client("s3")
    try:
        s3_client.upload_file(file_path, bucket_name, s3_key)
        print(f"Uploaded to S3 {s3_key}")
        return True
    except Exception as e:
        print("Error uploading to S3:", str(e))
        return False


def lambda_handler(event, context):
    body = json.loads(event["Records"][0]["body"])
    media_url, language, sub_language, pusher_channel = (
        body["media_url"],
        body["language"],
        body["sub_language"],
        body["pusher_channel"],
    )

    sqs_client = boto3.client(
        "sqs",
        region_name=get_parameter(AWS_REGION_NAME),
    )

    # Initialize Pusher
    pusher = Pusher(
        app_id=get_parameter(PUSHER_APP_ID),
        key=get_parameter(PUSHER_KEY),
        secret=get_parameter(PUSHER_SECRET),
        cluster=get_parameter(PUSHER_CLUSTER),
        ssl=True,
    )

    try:
        pusher.trigger(
            pusher_channel, "job-update", {"progress": "Downloading file from youtube"}
        )
        # Download the YouTube video
        download_path = os.path.join("/", "tmp")
        print("Downloading from youtube")
        if download_youtube_video(media_url, download_path, pusher_channel + ".mp4"):
            # Upload the downloaded video to S3
            s3_bucket_name = "quick-translates"
            s3_key = os.path.join("user_uploads", pusher_channel + ".mp4")
            pusher.trigger(
                pusher_channel, "job-update", {"progress": f"Uploading file to S3"}
            )
            print("Uploading to S3")
            if upload_file_to_s3(
                os.path.join(download_path, pusher_channel + ".mp4"),
                s3_bucket_name,
                s3_key,
            ):
                # Prepare message for the SQS queue
                message_body = {
                    "file_uri": f"s3://{s3_bucket_name}/{s3_key}",
                    "language": language,
                    "sub_language": sub_language,
                    "pusher_channel": pusher_channel,
                }

                # Send a message to the SQS queue
                sqs_client.send_message(
                    QueueUrl=get_parameter(WORKER_QUEUE_URL),
                    MessageBody=json.dumps(message_body),
                )

                # Delete the message after processing is complete
                sqs_client.delete_message(
                    QueueUrl=get_parameter(YOUTUBE_QUEUE_URL),
                    ReceiptHandle=json.loads(event["Records"][0]["receiptHandle"]),
                )

                # Respond to the client with a 202 status code and job_id
                return {"statusCode": 202, "body": json.dumps({"status": "Accepted"})}
            else:
                return {
                    "statusCode": 500,
                    "body": json.dumps({"error": "Failed to upload video to S3."}),
                }
        else:
            return {
                "statusCode": 500,
                "body": json.dumps({"error": "Failed to download video from YouTube."}),
            }

    except Exception as e:
        # Handle exceptions and errors gracefully
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "An error occurred: " + str(e)}),
        }
