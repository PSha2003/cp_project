# dlp/queue_clients.py
import aioboto3
import asyncio
import redis.asyncio as redis
import json

class QueueClient:
    async def get_messages(self):
        raise NotImplementedError


class SQSQueueClient(QueueClient):
    def __init__(self, queue_url, region="us-east-1"):
        self.queue_url = queue_url
        self.region = region
        self.session = aioboto3.Session(profile_name="default")

    async def get_messages(self):
        async with self.session.client('sqs', region_name=self.region) as client:
            response = await client.receive_message(
                QueueUrl=self.queue_url,
                MaxNumberOfMessages=10,
                WaitTimeSeconds=5
            )
            return response.get('Messages', [])

    async def add_message(self, message):
        async with self.session.client('sqs', region_name=self.region) as client:
            await client.send_message(
                QueueUrl=self.queue_url,
                MessageBody=message
            )


class InMemoryQueueClient(QueueClient):
    def __init__(self):
        self.queue = asyncio.Queue()

    async def add_message(self, message):
        await self.queue.put(message)

    async def get_messages(self):
        messages = []
        while not self.queue.empty():
            messages.append(await self.queue.get())
        return messages

class RedisQueueClient:
    def __init__(self, redis_url="redis://redis:6379", queue_name="dlp-tasks"):
        self.redis_url = redis_url
        self.queue_name = queue_name
        self.redis = redis.from_url(self.redis_url)

    async def add_message(self, message):
        await self.redis.rpush(self.queue_name, message)

    async def get_messages(self, count=10):
        messages = []
        for _ in range(count):
            msg = await self.redis.lpop(self.queue_name)
            if msg:
                messages.append({"Body": msg.decode("utf-8")})
        return messages

