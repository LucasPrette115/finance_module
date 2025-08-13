import uuid


class Transaction:
    def __init__(self, date, description=None, document=None, status=None, credit=0, debit=0, account_id=None, category_id=None):
        self.id = uuid.uuid4()
        self.date = date
        self.description = description
        self.document = document
        self.status = status
        self.credit = credit
        self.debit = debit
        self.account_id = account_id
        self.category_id = category_id