from pydantic import BaseModel, Field
from datetime import datetime
from typing import Any, Dict, List

class Event(BaseModel):
    topic: str = Field(..., example="sensor-data")
    event_id: str = Field(..., example="uuid-12345")
    timestamp: datetime
    source: str
    payload: Dict[str, Any]

class EventBatch(BaseModel):
    events: List[Event]