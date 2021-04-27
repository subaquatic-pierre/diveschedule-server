import json


def parse_response(response):
    content = json.loads(response.content)
    return content.get("data")


def print_data(data):
    print(json.dumps(data, indent=4))


def assert_no_errors(response):
    errors = response.errors
    assert not errors, f"Response has error: {response.errors}"