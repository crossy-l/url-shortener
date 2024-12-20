import uuid

def generate_truncated_uuid(length: int = 8):
    return uuid.uuid4().hex[:length]