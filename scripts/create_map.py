import os
import requests

ISSUE_NUMBER = os.getenv("ISSUE_NUMBER")
ISSUE_BODY = os.getenv("ISSUE_BODY")

print(f"ISSUE_NUMBER: {ISSUE_NUMBER}")
print(f"ISSUE_BODY: {ISSUE_BODY}")
