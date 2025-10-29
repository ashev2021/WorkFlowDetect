SUPPORTED_APPS = [
    {"app_id": 1, "app_name": "gmail", "app_type": "public", "app_description": "Send emails with Google Mail."},
    {"app_id": 2, "app_name": "slack", "app_type": "public", "app_description": "Send and receive messages."},
    {"app_id": 3, "app_name": "hubspot", "app_type": "public", "app_description": "Track leads in Hubspot CRM."}
]

SUPPORTED_ACTIONS = [
    {"action_id": 1, "app_id": 1, "action_name": "send_email", "action_description": "Send a new email."},
    {"action_id": 2, "app_id": 1, "action_name": "forward_email", "action_description": "Forward an existing email."},
    {"action_id": 3, "app_id": 1, "action_name": "apply_label", "action_description": "Apply a label to an email."},
    {"action_id": 4, "app_id": 2, "action_name": "send_message", "action_description": "Send a message to a Slack channel."},
    {"action_id": 5, "app_id": 3, "action_name": "create_contact", "action_description": "Create a new contact in Hubspot."}
]

def is_supported_app(app_name: str) -> bool:
    return any(app["app_name"] == app_name and app["app_type"] == "public" for app in SUPPORTED_APPS)

def is_supported_action(app_name: str, action_name: str) -> bool:
    app = next((app for app in SUPPORTED_APPS if app["app_name"] == app_name), None)
    if not app:
        return False
    return any(
        action["app_id"] == app["app_id"] and action["action_name"] == action_name
        for action in SUPPORTED_ACTIONS
    )
