import uuid


def is_uuid4(s: str) -> bool:
    try:
        return uuid.UUID(s).version == 4
    except ValueError:
        return False
