from API_keys import *
import oneai
import requests
import time
import json
from urllib.parse import urlencode

oneai.api_key = ONE_AI_KEYS.oneai_key
api_key = ONE_AI_KEYS.oneai_key

inputed_path = str(input('Please input the full path of the file: '))
with open(inputed_path, "rb") as f:
  text = f.read()

pipeline = {
  "input_type": "article",
  "steps": [
    {
      "skill": "pdf-extract-text"
    },
    {
      "skill": "summarize"
    },
    {
      "skill": "highlights"
    },
    {
      "skill": "article-topics"
    },
    {
      "skill": "keywords"
    }
  ],
  "content_type": "text/pdf"
}
url = "https://api.oneai.com/api/v0/pipeline/async/file?" + urlencode({"pipeline": json.dumps(pipeline)})

headers = {
  "api-key": api_key,
  "content-type": "text/pdf"
}

r = requests.post(url, text, headers=headers)
data = r.json()

get_url = f"https://api.oneai.com/api/v0/pipeline/async/tasks/{data['task_id']}"
while (True):
  r = requests.get(get_url, headers=headers)
  response = r.json()

  if response['status'] != "RUNNING":
    break

  time.sleep(5)

print(response)

