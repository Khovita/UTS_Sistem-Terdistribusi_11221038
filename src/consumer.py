import asyncio
import logging
from datetime import datetime

logger = logging.getLogger("consumer")

class Consumer:
    def __init__(self, queue, dedup_store):
        self.queue = queue
        self.dedup_store = dedup_store
        self.processed_events = []
        self.stats = {"received": 0, "unique_processed": 0, "duplicate_dropped": 0, "start_time": datetime.utcnow()}

    async def start(self):
        while True:
            event = await self.queue.get()
            self.stats["received"] += 1

            if self.dedup_store.is_duplicate(event.topic, event.event_id):
                self.stats["duplicate_dropped"] += 1
                logger.info(f"Duplicate detected: {event.topic}-{event.event_id}")
            else:
                self.dedup_store.add_event(event.topic, event.event_id)
                self.stats["unique_processed"] += 1
                self.processed_events.append(event)
                logger.info(f"Processed: {event.topic}-{event.event_id}")

            self.queue.task_done()
