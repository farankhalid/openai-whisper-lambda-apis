import boto3
import json

ses = boto3.client("ses")


def lambda_handler(event, context):
    email_address = event["email"]
    s3_uri = event["s3_uri"]

    template_name = "QuickTranslatesTemplate"

    template_data = {
        "s3_uri": s3_uri,
    }

    try:
        response = ses.send_templated_email(
            Source="bonjour@quicktranslates.com",
            Destination={"ToAddresses": [email_address]},
            Template=template_name,
            TemplateData=json.dumps({"s3_uri": f"{s3_uri}"}),
        )
        return {"statusCode": 200, "body": json.dumps("Email sent successfully!")}
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps("Error sending email: " + str(e))}
