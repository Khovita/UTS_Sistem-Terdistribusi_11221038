from fastapi import FastAPI, HTTPException
import asyncio
from src.models import Event, EventBatch
from src.dedup_store import DedupStore
from src.consumer import Consumer
from datetime import datetime

app = FastAPI(title="UTS Pub-Sub Log Aggregator")

# Components
queue = asyncio.Queue()
dedup_store = DedupStore()
consumer = Consumer(queue, dedup_store)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(consumer.start())

@app.post("/publish")
async def publish_events(batch: EventBatch):
    for event in batch.events:
        await queue.put(event)
    return {"status": "queued", "count": len(batch.events)}

@app.get("/events")
def get_events(topic: str = None):
    if topic:
        events = [e for e in consumer.processed_events if e.topic == topic]
    else:
        events = consumer.processed_events
    return {"count": len(events), "events": [e.dict() for e in events]}

@app.get("/stats")
def get_stats():
    uptime = (datetime.utcnow() - consumer.stats["start_time"]).total_seconds()
    return {**consumer.stats, "uptime_seconds": uptime}
