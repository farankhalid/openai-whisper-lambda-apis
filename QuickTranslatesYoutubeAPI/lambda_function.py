import json
import boto3
import uuid
import os
from pusher import Pusher
from config import (
    get_parameter,
    AWS_REGION_NAME,
    PUSHER_APP_ID,
    PUSHER_KEY,
    PUSHER_SECRET,
    PUSHER_CLUSTER,
    YOUTUBE_QUEUE_URL,
)


def lambda_handler(event, context):
    # Get uploaded file and language from the event payload
    media_url = event.get("media_url")
    language = event.get("language")
    sub_language = event.get("sub_language")

    # Validate the uploaded file and language
    if not media_url:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "No file URI provided."}),
        }
    if not language:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "No media language provided."}),
        }
    if not sub_language:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "No subtitle language provided."}),
        }

    pusher_channel = str(uuid.uuid4()).replace("-", "")

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

    pusher.trigger(pusher_channel, "job-update", {"progress": "Creating job request."})

    try:
        # Prepare message for the SQS queue
        message_body = {
            "media_url": media_url,
            "language": language,
            "sub_language": sub_language,
            "pusher_channel": pusher_channel,
        }

        # Send a message to the SQS queue
        sqs_client.send_message(
            QueueUrl=get_parameter(YOUTUBE_QUEUE_URL),
            MessageBody=json.dumps(message_body),
        )

        # Respond to the client with a 202 status code and pusher_channel
        return {
            "statusCode": 202,
            "body": json.dumps(
                {"status": "Accepted", "pusher_channel": pusher_channel}
            ),
        }

    except Exception as e:
        # Handle exceptions and errors gracefully
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "An error occurred: " + str(e)}),
        }
