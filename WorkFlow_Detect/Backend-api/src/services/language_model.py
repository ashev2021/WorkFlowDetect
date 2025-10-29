import os
import openai
import asyncio
from dotenv import load_dotenv
from openai import OpenAI



class LLMService:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OpenAI API key not set. Please set 'OPENAI_API_KEY'.")
        self.client = OpenAI(api_key=api_key)

    async def call_llm(self, step_description: str):
        prompt = f"""
You are an assistant mapping plain text workflow step descriptions to a supported app and action.

Supported apps and their public actions:
- gmail: send_email, forward_email, apply_label
- slack: send_message
- hubspot: create_contact

Do NOT suggest any private or unsupported apps or actions.
If the description does not describe a workflow step, reply with 
{{"app_name": null, "action_name": null}}.

Step description: "{step_description}"

Return a JSON object like:

{{
"app_name": "",
"action_name": ""
}}

If no valid app/action is found, or the input is not a step description, return null for both.
"""

        def sync_openai_call():
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You map workflow steps to apps and actions."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0,
            )
            return response.choices[0].message.content.strip()

        text_resp = await asyncio.to_thread(sync_openai_call)

        import json
        try:
            return json.loads(text_resp)
        except json.JSONDecodeError:
            return {"app_name": None, "action_name": None}
