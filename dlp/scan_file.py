# scan_file.py
from .models import Pattern, Message
from asgiref.sync import sync_to_async
import re

@sync_to_async
def get_patterns():
    return list(Pattern.objects.all())

@sync_to_async
def save_match(pattern, file_name, match):
    return Message.objects.create(
        pattern=pattern,
        file_name = file_name,
        content=match
    )

async def scan_file_for_sensitive_data(file_path):
    patterns = await get_patterns()
    matches = []
    print(patterns)

    with open(file_path, 'r') as f:
        content = f.read()

    for pattern in patterns:
        print(pattern.regex)
        regex = re.compile(pattern.regex)
        found = regex.findall(content)
        print(content)
        print(found)
        for match in found:
            print(f"Match found for {pattern.name} in message: {content}")
            await save_match(pattern, file_path, match)
            matches.append(match)

    return matches

