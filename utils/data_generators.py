import uuid

def unique_id():
    return str(uuid.uuid4())[:8]

def random_integration_name():
    return f"integration_{unique_id()}"

def random_asset_name():
    return f"asset_{unique_id()}"
