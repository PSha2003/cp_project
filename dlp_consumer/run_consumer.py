# run_consumer.py
import asyncio
import logging
from dlp_consumer.consumer import Manager
from dlp.tasks import scan_message
from dlp.shared_queue import queue_client
from dlp.scan_file import scan_file_for_sensitive_data

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

async def main():
    # Add fake test message
    #await queue_client.add_message('{"task": "scan_message", "args": ["My test message 1234567812345678"], "kwargs": {"user":"chel", "ts":"100001.1212", "channel":"0000000"}}')

    try:
        manager = Manager(queue_client, tasks={
            "scan_message": scan_message, "scan_file": scan_file_for_sensitive_data
        })

        await manager.main()
    except Exception as e:
        logger.exception(f"Unexpected error in main execution: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())

