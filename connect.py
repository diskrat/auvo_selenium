import urllib.request
import json
import urllib.error

from settings import AUVO_API_TOKEN

API_URL = "https://api.auvo.com.br/v2/questionnaires/153680"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {AUVO_API_TOKEN}",
}
req = urllib.request.Request(API_URL, headers=headers)

try:
    with urllib.request.urlopen(req) as response:
        data = response.read().decode("utf-8")  # Parse JSON
        # only get the data inside result
        json_data = json.loads(data)["result"][0]
        keys_to_keep = ["id", "description", "answerType"]
        json_data["questions"] = [
            dict((k, v) 
            for k, v in item.items() if k in keys_to_keep)
            for item in json_data["questions"]
        ]
        json_data = {k: v for k, v in json_data.items() if k in ['id','questions']}
        with open("questionnaires.json", "w", encoding="utf-8") as json_file:
            json.dump(json_data, json_file, ensure_ascii=False, indent=4)
except urllib.error.HTTPError as e:
    print(f"HTTP Error {e.code}: {e.reason}")
except urllib.error.URLError as e:
    print("URL Error:", e.reason)
