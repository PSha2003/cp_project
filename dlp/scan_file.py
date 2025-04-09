# scan_file.py
import re
import logging
from .models import Pattern, Message
from asgiref.sync import sync_to_async

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

@sync_to_async
def get_patterns():
    return list(Pattern.objects.all())

@sync_to_async
def save_match(pattern, file_name, match):
    try:
        return Message.objects.create(
            pattern=pattern,
            file_name = file_name,
            content=match
        )
    except Exception as e:
        logger.error(f"Error saving match for pattern {pattern.name} in file {file_name}: {e}")

async def scan_file_for_sensitive_data(file_path):
    logger.info(f"Scanning file for sensitive data: {file_path}")
    patterns = await get_patterns()

    if not patterns:
        logger.warning("No patterns found in the database.")
        return []

    matches = []

    with open(file_path, 'r') as f:
        content = f.read()

    for pattern in patterns:
        try:
            regex = re.compile(pattern.regex)
            found = regex.findall(content)
            for match in found:
                logger.info(f"Match found for {pattern.name} in file: {file_path}")
                await save_match(pattern, file_path, match)
                matches.append(match)
        except Exception as e:
            logger.error(f"Unexpected error while scanning file {file_path} with pattern {pattern.name}: {e}")

    return matches

