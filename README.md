# Ardoq Devops Intern Challenge
## Task 1
How would you parse it to find if the oldest timestamp is older than 1 hour than the current time. If it is older to trigger some alarm of your choice slack message or email.

Personaly i think i would AWS or some other cloud service for a task like this. For this to work i would like the .data file to be in a S3 bucket and make the service, which outputted this log data file, to write to the S3 bucket.

Why a S3 bucket? This is because we can create a aws lambda function with the S3 bucket as its trigger. This lambda function would:

1. Read the content of the S3 bucket, which is the .data file
2. Parse the content to a format easier to work with, such as an object
3. Trigger som alarm
    a. If the alarm is a slack message you could create a slackbot with enabled webhooks. This way we can easily post a message on slack through a POST request, where the url probably should be an envoriment variable.
    b. If the alarm is a mail we can simply use boto3 to send mail with AWS SES.

For this task i've decided to send a mail. I've created a small lambda function in the ![task1](./task1) folder which can be deployed through the serverless. One could see in the ![yaml file](./serverless.yml) that this function triggers on all changes to the bucket "ardoqdata". 

On trigger the lambda function will first retrieve the data from the file in the bucket. Then it will go through a parser. 

You can find the whole file ![here](./parser.py).

First part of the parser is making the string a little bit more workable.

This python lambda function creates a list from a string. It extracts everything between the two curly brackets which comes after ":cluster-time {...}". The outcome is `[":time 1573573493, :id 6509638591, :inc 2", ":time 1573637584, ..." ]`
```python
    cleaned_data = list(
        map(lambda match: match[1], re.findall(r"(:cluster-time\s\{(.*?)\})", data))
    )
```

The second part of the parser will loop through this list, split it on commas and use regex to extract key value pairs. They have the format `:key pair`, for example `:id 123`. Then it creates an object, pushes it to entries and returns a list of objects.
```python
    entries = []
    for entry in cleaned_data:
        properties = entry.split(",")
        entry_obj = {}
        for prop in properties:
            matches = re.search(r":(\w+)\s(\d+)", prop)
            key = matches.group(1)
            value = int(matches.group(2))
            entry_obj[key] = value
        entries.append(entry_obj)
    return entries
```

The rest of the handler will check for the oldest entry. I assumed the time prop were most likely in Unix time format (seconds passed since 1 January 1970). I used time.ctime() on one of the entries and got "Tue Nov 12 16:44:53 2019". If it is older it will send a mail. The sendmail function is more or less a very basic python function which uses standard functionality to send mail. The recipient and sender is based on the envoriment variables we set on AWS lambda.
```python
    oldest_entry = max(parsed_data, key=lambda x: x["time"])
    is_older = oldest_entry["time"] - time.time() > 60 * 60
    print(f"Oldest timestamp: {time.ctime(oldest_entry['time'])}")
    print(f"Oldest timestamp is 1 hour older than current time: {is_older}")
    if is_older:
        sendmail(oldest_entry
```
