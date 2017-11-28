
import uuid


def create_unique_env_name():
    return str(uuid.uuid4()).replace('-', '_')
