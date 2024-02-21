import boto3


def get_parameter(parameter_name):
    ssm = boto3.client("ssm")

    response = ssm.get_parameter(Name=parameter_name, WithDecryption=True)

    return response["Parameter"]["Value"]


# AWS Parameter Store parameter names
AWS_REGION_NAME = "/openai-whisper/AWS_REGION_NAME"
PUSHER_APP_ID = "/openai-whisper/PUSHER_APP_ID"
PUSHER_KEY = "/openai-whisper/PUSHER_KEY"
PUSHER_SECRET = "/openai-whisper/PUSHER_SECRET"
PUSHER_CLUSTER = "/openai-whisper/PUSHER_CLUSTER"
WORKER_QUEUE_URL = "/openai-whisper/WORKER_QUEUE_URL"
