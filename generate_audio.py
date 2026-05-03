import json
import os
import time
import requests

AZURE_KEY = "Y1u5oqird7ygUmscl0gfDR5t1cn3Td7zDgxmU9YMrMWjIcC8BDcR8JQQJ99BIACYeBjFXJ3w3AAAYACOGhDql"
AZURE_REGION = "eastus"

url = f"https://{AZURE_REGION}.tts.speech.microsoft.com/cognitiveservices/v1"

headers = {
    "Ocp-Apim-Subscription-Key": AZURE_KEY,
    "Content-Type": "application/ssml+xml",
    "X-Microsoft-OutputFormat": "audio-16khz-128kbitrate-mono-mp3"
}

voices = [
    ("en-GB-RyanNeural", "GB_Male"),
    ("en-GB-LibbyNeural", "GB_Female"),
    ("en-US-GuyNeural", "US_Male"),
    ("en-US-JennyNeural", "US_Female")
]

with open("idioms_master.json", "r", encoding="utf-8") as f:
    idioms = json.load(f)

for index, item in enumerate(idioms):
    voice_name, voice_label = voices[index % len(voices)]

    safe_name = (
        item["idiom"]
        .replace(" ", "_")
        .replace("’", "")
        .replace("'", "")
        .replace(",", "")
        .replace("?", "")
        .replace("!", "")
    )

    filename = f"audio/{item['id']}_{voice_label}_{safe_name}.mp3"

    if os.path.exists(filename):
        print(f"Skipping: {filename}")
        continue

    text = f"{item['idiom']}. {item['idiom']}."

    ssml = f"""
<speak version='1.0' xml:lang='en-US'>
  <voice name='{voice_name}'>
    {text}
  </voice>
</speak>
"""

    response = requests.post(url, headers=headers, data=ssml.encode("utf-8"))

    if response.status_code == 200:
        with open(filename, "wb") as f:
            f.write(response.content)
        print(f"Saved: {filename}")
    else:
        print(f"Error for {item['id']} {item['idiom']}: {response.status_code} {response.text}")

    time.sleep(1.5)