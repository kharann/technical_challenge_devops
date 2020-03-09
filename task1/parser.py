import re

"""
This function takes in the data from the S3 bucket and converts it into the format of:

entries = [{ "id":int, "time":int, "inc":int }, ...]
"""


def parse(data):
    cleaned_data = list(
        map(lambda match: match[1], re.findall(r"(:cluster-time\s\{(.*?)\})", data))
    )

    entries = []

    # Splits and extracts all (:key value) pairs from the string and appends them to a list of entries
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
