import os
import django

#import sys
#sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cp_project.settings")
django.setup()

import asyncio
import json
import re
import aiohttp
from dlp.tasks import scan_message

class Manager:
    def __init__(self, queue_name: str, tasks: dict):
#        self.loop = asyncio.get_event_loop()
        self.queue = queue_name
        self.tasks = tasks

    async def process_messages(self):
        while True:
            messages = await self.queue.get_messages()
            #print(f"📥 Got {len(messages)} messages")
            tasks_to_run = []  # List to hold all tasks
            for message in messages:
                try:
                    body = json.loads(message['Body']) if isinstance(message, dict) else json.loads(message)
                except Exception as e:
                    print(f"Invalid message format: {e}")
                    continue

                task_name = body.get('task')
                args = body.get('args', ())
                kwargs = body.get('kwargs', {})
                task = self.tasks.get(task_name)
                if task:
                   #await self.loop.create_task(task(*args, **kwargs))
                   # Instead of creating a task immediately, append it to the tasks list
                   #tasks_to_run.append(self.loop.create_task(task(*args, **kwargs)))
                   tasks_to_run.append(task(*args, **kwargs))
                else:
                    print(f"No such task: {task_name}")

            if tasks_to_run:
                # Run all tasks concurrently and wait for them to finish
                await asyncio.gather(*tasks_to_run)

            await asyncio.sleep(1)


    async def main(self):
        await self.process_messages()

