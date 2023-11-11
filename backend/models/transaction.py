# backend/models/transaction.py

class Transaction:
    def __init__(self, sender, recipient, amount, timestamp):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.timestamp = timestamp
