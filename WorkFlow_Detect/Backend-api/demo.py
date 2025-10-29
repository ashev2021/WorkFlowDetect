import requests

API_URL = "http://127.0.0.1:8000/suggest_steps"

examples = [
    "Send a welcome email to new leads using Gmail",
    "Post a message to a Slack channel",
    "Random text not a workflow"
]

payload = {"workflow_step_descriptions": examples}

response = requests.post(API_URL, json=payload)

print(f"Input descriptions:\n{examples}\n")
print(f"API response:\n{response.json()}")
