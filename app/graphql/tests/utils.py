import json


def parse_response(response):
    content = json.loads(response.content)
    return content.get("data")


def print_data(data):
    print(json.dumps(data, indent=4))