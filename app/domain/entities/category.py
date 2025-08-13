import uuid


class Category:
    def __init__(self, name, type, parent_id=None, description=None):
        self.id = uuid.uuid4()
        self.name = name
        self.type = type
        self.parent_id = parent_id
        self.description = description

    