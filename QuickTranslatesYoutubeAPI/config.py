import boto3


def get_parameter(parameter_name):
    ssm = boto3.client("ssm")

    response = ssm.get_parameter(Name=parameter_name, WithDecryption=True)

    return response["Parameter"]["Value"]


# AWS Parameter Store parameter names
AWS_REGION_NAME = "/quick-translates/AWS_REGION_NAME"
PUSHER_APP_ID = "/quick-translates/PUSHER_APP_ID"
PUSHER_KEY = "/quick-translates/PUSHER_KEY"
PUSHER_SECRET = "/quick-translates/PUSHER_SECRET"
PUSHER_CLUSTER = "/quick-translates/PUSHER_CLUSTER"
YOUTUBE_QUEUE_URL = "/quick-translates/YOUTUBE_QUEUE_URL"
