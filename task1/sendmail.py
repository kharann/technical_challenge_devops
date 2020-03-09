import boto3
import os
from time import ctime
from botocore.exceptions import ClientError


def sendmail(oldest_entry):
    SENDER = os.environ("SENDER")

    RECIPIENT = os.environ("RECIPIENT")

    SUBJECT = f"Oldest cluster is 1 hour older than the current time"

    BODY_TEXT = (
        "Oldest cluster: \n"
        f"Id: {oldest_entry['id']}, time: {ctime(oldest_entry['timestamp'])}, inc: {oldest_entry['inc']} "
    )

    client = boto3.client("ses", region="eu-west-1")
    try:
        response = client.send_email(
            Destination={"ToAddresses": [RECIPIENT,],},
            Message={
                "Body": {"Text": {"Charset": "UTF-8", "Data": BODY_TEXT,},},
                "Subject": {"Charset": "UTF-8", "Data": SUBJECT,},
            },
            Source=SENDER,
        )
        print("Email sent! Message ID:")
        print(response["MessageId"])
    # Display an error if something goes wrong.
    except ClientError as e:
        print(e.response["Error"]["Message"])

