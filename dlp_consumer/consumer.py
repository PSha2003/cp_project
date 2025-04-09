import os
import django
import asyncio
import json
import re
import logging
import aiohttp

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cp_project.settings")
django.setup()

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

from dlp.tasks import scan_message

class Manager:
    def __init__(self, queue_name: str, tasks: dict):
        self.queue = queue_name
        self.tasks = tasks

    async def process_messages(self):
        while True:
            try:
                messages = await self.queue.get_messages()
                if len(messages) > 0: logger.info(f"📥 Received {len(messages)} messages")
                tasks_to_run = []  # List to hold all tasks
                for message in messages:
                    try:
                        body = json.loads(message['Body']) if isinstance(message, dict) else json.loads(message)
                    except Exception as e:
                        logger.error(f"Invalid message format: {e}")
                        continue

                    task_name = body.get('task')
                    args = body.get('args', ())
                    kwargs = body.get('kwargs', {})
                    task = self.tasks.get(task_name)

                    if task:
                        try:
                            tasks_to_run.append(task(*args, **kwargs))
                        except Exception as e:
                            logger.exception(f"Failed to create task '{task_name}': {e}")
                    else:
                        logger.warning(f"No such task registered: {task_name}")

                if tasks_to_run:
                    # Run all tasks concurrently and wait for them to finish
                    await asyncio.gather(*tasks_to_run)
            except Exception as e:
                logger.exception(f"Unexpected error while processing messages: {e}")

            await asyncio.sleep(1)


    async def main(self):
        await self.process_messages()

