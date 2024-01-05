import uuid


def random_session_id() -> str:
    return str(uuid.uuid4())