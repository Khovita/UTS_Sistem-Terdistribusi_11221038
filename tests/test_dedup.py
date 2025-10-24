import os
import pytest
from src.dedup_store import DedupStore

@pytest.fixture
def tmp_store(tmp_path):
    db_file = tmp_path / "dedup_test.db"
    return DedupStore(db_path=str(db_file))

def test_add_and_check_duplicate(tmp_store):
    topic = "test-topic"
    event_id = "evt-123"

    # Awalnya belum ada
    assert not tmp_store.is_duplicate(topic, event_id)

    # Tambahkan event pertama kali
    tmp_store.add_event(topic, event_id)

    # Sekarang harus terdeteksi duplikat
    assert tmp_store.is_duplicate(topic, event_id)

def test_persistence_across_restart(tmp_path):
    db_file = tmp_path / "persist.db"
    store1 = DedupStore(db_path=str(db_file))
    store1.add_event("test", "abc-123")

    # Simulasikan restart (buat instance baru)
    store2 = DedupStore(db_path=str(db_file))
    assert store2.is_duplicate("test", "abc-123")
