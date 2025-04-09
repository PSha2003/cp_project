import json
import re
import requests
import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import Pattern, Message
from .shared_queue import queue_client

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

@csrf_exempt
async def slack_event_hook(request):
    try:
       body = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        logger.error("Invalid JSON received in slack_event_hook")
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    if body.get('type') == 'url_verification':
        return JsonResponse({'challenge': body['challenge']})


    event = body.get('event', {})

    if event.get('type') == 'message' and 'subtype' not in event:
        user = event.get('user')
        content = event.get('text')
        ts = event.get('ts')
        channel = event.get('channel')

        # Basic validation
        if not all([user, content, ts, channel]):
            logger.warning("Missing required fields in message: user=%s, content=%s, ts=%s, channel=%s", user, content, ts, channel)
            return JsonResponse({'error': 'Missing required message fields'}, status=400)

        if not isinstance(content, str) or len(content.strip()) == 0:
            logger.warning("Invalid message content: %s", content)
            return JsonResponse({'error': 'Empty or invalid message content'}, status=400)

        task_payload = json.dumps({
                "task": "scan_message",
                "args": [content],
                "kwargs": {"user":user, "ts":ts, "channel":channel}
            })
        try:
            await queue_client.add_message(task_payload)
        except Exception as e:
            logger.error("Failed to enqueue message: %s", str(e))
            return JsonResponse({'error': 'Internal queue error'}, status=500)


    return JsonResponse({'ok': True})

@require_http_methods(["GET"])
def get_patterns(request):
    patterns = list(Pattern.objects.values("name", "regex"))
    return JsonResponse({"patterns": patterns})

@require_http_methods(["POST"])
def save_match(request):
    try:
        body = json.loads(request.body)
        pattern = Pattern.objects.get(name=body["pattern"])
        Message.objects.create(
            user=body["user"],
            content=body["content"],
            slack_ts=body["ts"],
            pattern=pattern
        )
    except Exception as e:
        logger.error("Error saving match: %s", str(e))
        return JsonResponse({"error": "Internal server error"}, status=500)

    return JsonResponse({"ok": True})
