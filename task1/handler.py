import boto3
from .parser import parse
from .sendmail import sendmail
import time


def trigger_alarm(event, context):
    s3 = boto3.resource("s3")
    obj = s3.Object("ardoqdata", "daemonEDN.data")
    data = obj.get()["Body"].read().decode("utf-8")

    parsed_data = parse(data)
    oldest_entry = max(parsed_data, key=lambda x: x["time"])
    is_older = oldest_entry["time"] - time.time() > 60 * 60
    print(f"Oldest timestamp: {time.ctime(oldest_entry['time'])}")
    print(f"Oldest timestamp is 1 hour older than current time: {is_older}")
    if is_older:
        sendmail(oldest_entry)
