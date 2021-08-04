import base64
import os
import requests
from uuid import uuid1
from ghapi.all import GhApi

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
ISSUE_NUMBER = os.getenv("ISSUE_NUMBER")
ISSUE_BODY = os.getenv("ISSUE_BODY")
MAPBOX_API_KEY = os.getenv("MAPBOX_API_KEY")

# Parse body string to dictionary
split_body = [i.strip('### ') for i in ISSUE_BODY.strip('\n').split("\n\n")]

body_dict = {}
for i in range(0, len(split_body), 2):
    body_dict[split_body[i]] = split_body[i+1]

lng = body_dict["Longitude"]
lat = body_dict["Latitude"]

mapbox_url = f"https://api.mapbox.com/styles/v1/mapbox/streets-v11/static/{lng},{lat},9.31,0/300x200?access_token={MAPBOX_API_KEY}"
response = requests.get(mapbox_url)

data = response.content
b64data = [base64.b64encode(data).decode('ascii')]

cur_uuid = uuid1()
path = f"images/{cur_uuid}.png"
message = f"add file: {cur_uuid}"

api = GhApi(owner='darrenwiens', repo='issue-mapper', token=GITHUB_TOKEN)
api.repos.create_or_update_file_contents(path, message=message, content=b64data[0])

map_center_text = "Map Centered at ({lat}, {lng})"
img_link = f"![{map_center_text}](/{path} "")"
body = f"### Map Result\n\n{map_center_text}\n\n{img_link}"
api.issues.create_comment(ISSUE_NUMBER, body)
