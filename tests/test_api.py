import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_publish_and_dedup():
    event = {
        "events": [{
            "topic": "sensor",
            "event_id": "e123",
            "timestamp": "2025-10-21T10:00:00Z",
            "source": "sensor-1",
            "payload": {"temp": 27.5}
        }]
    }

    res1 = client.post("/publish", json=event)
    res2 = client.post("/publish", json=event)
    assert res1.status_code == 200
    assert res2.status_code == 200

    stats = client.get("/stats").json()
    assert stats["received"] >= 2
    assert stats["unique_processed"] == 1
    assert stats["duplicate_dropped"] >= 1
