import json
import os
import urllib.parse as urlparse

import requests

API_VERSION = "v2"
BASE_API_URL = f"https://trackapi.nutritionix.com/{API_VERSION}/"
API_HEADERS = {
    'x-app-id': os.environ["NUTRITIONIX_API_ID"],
    'x-app-key': os.environ["NUTRITIONIX_API_KEY"],
    'x-remote-user-id': "0"
}


def search(food, debug=False):
    endpoint = urlparse.urljoin(BASE_API_URL, "natural/nutrients")

    if debug:
        print(endpoint)

    response = requests.post(
        endpoint, headers=API_HEADERS, json={"query": food})

    if debug:
        print(response.status_code)

    if response.status_code == 404:
        print("Error retrieving data. Status code 404.")
        return '{"Status": 404}'

    return response.text


def pprint_json(text):
    json_text = json.loads(text)
    print(json.dumps(json_text, indent=1))


def print_label(text, *args):
    json_text = json.loads(text)

    label = ""

    for i in range(len(json_text['foods'])):
        label = f"Food Item: {json_text['foods'][i]['food_name'].capitalize()}\n"

        for stat in args:
            label += f"{stat.capitalize()}: {json_text['foods'][0]['nf_' + stat.replace(' ', '_')]}\n"
        
    print(label)

if __name__ == "__main__":
    while True:
        print("Enter an item to search for: ")
        item = input()
        if item.lower() == "q":
            break

        response_text = search(item)
        # pprint_json(response_text)
        print_label(response_text, 'calories', 'total fat', 'saturated fat', 'cholesterol', 'sodium', 'total carbohydrate')