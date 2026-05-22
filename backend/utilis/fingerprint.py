import hashlib
import json

def generate_fingerprint(idea, owner_id):
    """Generate SHA-256 fingerprint for an idea."""
    payload = {
        "title": idea.title,
        "raw_description": idea.raw_description,
        "created_at": idea.created_at.isoformat(),
        "owner_id": str(owner_id),
        "scanty_note": idea.scanty_note,
    }
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(',', ':')).encode()
    ).hexdigest()
