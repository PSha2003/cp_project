import re
from .models import Pattern, Message
from asgiref.sync import sync_to_async
import requests
import httpx
import logging

logger = logging.getLogger(__name__)
SLACK_BOT_TOKEN = ''


if not SLACK_BOT_TOKEN:
    logger.warning("SLACK_BOT_TOKEN is not set. Slack API calls will fail.")

@sync_to_async
def get_all_patterns():
    try:
        return list(Pattern.objects.all())
    except Exception as e:
        logger.error(f"Failed to fetch patterns: {e}")
        return []

@sync_to_async
def save_message_match(pattern, user, content, slack_ts):
    try:
        return Message.objects.create(
            user=user,
            content=content,
            slack_ts=slack_ts,
            pattern=pattern
        )
    except Exception as e:
        logger.error(f"Failed to save message match: {e}")

async def scan_message(text, **kwargs):
    user = kwargs.get('user')
    ts = kwargs.get('ts')
    channel = kwargs.get('channel')

    if not all([user, ts, channel]):
        logger.warning("Missing required fields in scan_message")
        return

    try:
        patterns = await get_all_patterns()
        for pattern in patterns:
            if re.search(pattern.regex, text):
                logger.info(f"Match found for {pattern.name} in message: {text}")
                await save_message_match(pattern, user, text, ts)

                if SLACK_BOT_TOKEN:
                    async with httpx.AsyncClient() as client:
                        response = await client.post(
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
                    if response.status_code != 200 or not response.json().get("ok"):
                        logger.error(f"Slack API update failed: {response.text}")
                break
    except Exception as e:
        logger.error(f"[ERROR] scan_message failed: {e}")
