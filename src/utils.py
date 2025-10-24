import hashlib
from datetime import datetime

def generate_event_id(payload: dict, timestamp: str) -> str:
    """
    Membuat event_id unik berbasis payload dan timestamp.
    Cocok untuk fallback jika publisher tidak menyediakan event_id.
    """
    raw = str(payload) + timestamp
    return hashlib.sha256(raw.encode()).hexdigest()

def iso_now() -> str:
    """Mengembalikan waktu ISO8601 saat ini (UTC)."""
    return datetime.utcnow().isoformat() + "Z"
