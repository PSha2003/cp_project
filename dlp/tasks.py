import re
from .models import Pattern, Message
from asgiref.sync import sync_to_async
import requests
import httpx

SLACK_BOT_TOKEN = ''

@sync_to_async
def get_all_patterns():
    return list(Pattern.objects.all())

@sync_to_async
def save_message_match(pattern, user, content, slack_ts):
    return Message.objects.create(
            user=user,
            content=content,
            slack_ts=slack_ts,
            pattern=pattern
    )

async def scan_message(text, **kwargs):
    print("this is "+text)
    user = kwargs.get('user')
    ts = kwargs.get('ts')
    channel = kwargs.get('channel')

    try:
        patterns = await get_all_patterns()
        for pattern in patterns:
            if re.search(pattern.regex, text):
                print(f"Match found for {pattern.name} in message: {text}")
                await save_message_match(pattern, user, text, ts)

                async with httpx.AsyncClient() as client:
                    await client.post(
                        "https://slack.com/api/chat.update",
                        headers={
                            "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
                            "Content-type": "application/json"
                        },
                        json={
                            "channel": channel,
                            "ts": ts,
                            "text": ":warning: Message blocked due to sensitive content."
                        }
                    )
                break
    except Exception as e:
        print(f"[ERROR] scan_message failed: {e}")
