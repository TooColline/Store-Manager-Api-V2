import json

def convert_json(response):
    """Converts the response data to a json format"""

    json_response = json.loads(response.data.decode('utf-8'))

    return json_response