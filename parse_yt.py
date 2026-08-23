import json
try:
    with open('video_metadata.json', 'r', encoding='utf-16') as f:
        data = json.load(f)
        print(f"TITLE: {data.get('title')}")
        print(f"CHANNEL: {data.get('uploader')}")
        print(f"DURATION: {data.get('duration')} sec")
        print(f"DESCRIPTION: {data.get('description')}")
except Exception as e:
    print(e)
