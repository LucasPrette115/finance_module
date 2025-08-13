import uuid


class Account:
    def __init__(self, name, description=None):
        self.id = uuid.uuid4()
        self.name = name
        self.description = description   