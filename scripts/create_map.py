import base64
import os
import requests
import sys

from uuid import uuid1
from ghapi.all import GhApi

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
ISSUE_NUMBER = os.getenv("ISSUE_NUMBER")
ISSUE_BODY = os.getenv("ISSUE_BODY")
MAPBOX_API_KEY = os.getenv("MAPBOX_API_KEY")

def create_issue_comment(api, issue_number, body):
    api.issues.create_comment(ISSUE_NUMBER, body)

owner = "darrenwiens"
repo = "issue-mapper"
api = GhApi(owner=owner, repo=repo, token=GITHUB_TOKEN)

# Parse body string to dictionary
split_body = [i.strip('### ') for i in ISSUE_BODY.strip('\n').split("\n\n")]

body_dict = {}
for i in range(0, len(split_body), 2):
    body_dict[split_body[i]] = split_body[i+1]

lng = body_dict["Longitude"]
lat = body_dict["Latitude"]
default_style = body_dict["Default Map Style"]
light_style = body_dict.get("Light Mode Map Style")
dark_style = body_dict.get("Dark Mode Map Style")
print(f'body_dict: {body_dict}')
print(f'default_style: {default_style}')
print(f'light_style: {light_style}')
print(f'dark_style: {dark_style}')

try:
    lngfloat = float(lng)
    latfloat = float(lat)
except ValueError:
    body = "Either Latitude or Longitude don't seem to be numeric. Please delete this issue and try a new one."
    create_issue_comment(api, ISSUE_NUMBER, body)
    sys.exit()

def get_map(style, lat, lng):
    mapbox_url = f"https://api.mapbox.com/styles/v1/mapbox/{style}/static/{lng},{lat},9.31,0/300x200?access_token={MAPBOX_API_KEY}"
    response = requests.get(mapbox_url)

    data = response.content
    b64data = [base64.b64encode(data).decode('ascii')]

    cur_uuid = uuid1()
    path = f"images/{cur_uuid}.png"
    message = f"add file: {cur_uuid}"

    api.repos.create_or_update_file_contents(path, message=message, content=b64data[0])

    img_path = f"https://github.com/{owner}/{repo}/raw/main/{path}"
    return img_path

default_img_path = get_map(default_style, lat, lng)
map_center_text = f"Map Centered at ({lat}, {lng})"
default_img_link = f"[![{map_center_text}]({default_img_path})]({default_img_path})"
# body = f"### Map Result\n\n{map_center_text}\n\n{default_img_link}"


body = "<picture>"
if light_style and light_style != "None":
    light_img_path = get_map(light_style, lat, lng)
    body += f'<source media="(prefers-color-scheme: light)" srcset="{light_img_path}">'
if dark_style and dark_style != "None":
    dark_img_path = get_map(dark_style, lat, lng)
    body += f'<source media="(prefers-color-scheme: dark)" srcset="{dark_img_path}">'
body += f"""
  <img alt="Fallback image description" src="{default_img_path}">
</picture>
"""

create_issue_comment(api, ISSUE_NUMBER, body)
