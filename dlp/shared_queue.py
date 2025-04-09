from dlp.queue_clients import InMemoryQueueClient, SQSQueueClient, RedisQueueClient

# Choose which client to use
use_real_sqs = False

# Replace with SQSQueueClient if using AWS
if use_real_sqs:
    queue_client = SQSQueueClient(queue_url="https://sqs.us-east-1.amazonaws.com/123456789012/your-queue-name")
else:
    #queue_client = InMemoryQueueClient()
    queue_client = RedisQueueClient()

