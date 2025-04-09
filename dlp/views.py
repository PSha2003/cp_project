import json
import re
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import Pattern, Message
from .shared_queue import queue_client
from asgiref.sync import async_to_sync


@csrf_exempt
async def slack_event_hook(request):
    try:
       body = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
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
            return JsonResponse({'error': 'Missing required message fields'}, status=400)

        if not isinstance(content, str) or len(content.strip()) == 0:
            return JsonResponse({'error': 'Empty or invalid message content'}, status=400)

        task_payload = json.dumps({
                "task": "scan_message",
                "args": [content],
                "kwargs": {"user":user, "ts":ts, "channel":channel}
            })
        try:
            await queue_client.add_message(task_payload)
        except Exception as e:
            print("Failed to enqueue message:", str(e))
            return JsonResponse({'error': 'Internal queue error'}, status=500)


    return JsonResponse({'ok': True})

@require_http_methods(["GET"])
def get_patterns(request):
    patterns = list(Pattern.objects.values("name", "regex"))
    return JsonResponse({"patterns": patterns})

@require_http_methods(["POST"])
def save_match(request):
    body = json.loads(request.body)
    pattern = Pattern.objects.get(name=body["pattern"])
    Message.objects.create(
        user=body["user"],
        content=body["content"],
        slack_ts=body["ts"],
        pattern=pattern
    )
    return JsonResponse({"ok": True})
