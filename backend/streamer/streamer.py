# backend/streamer/streamer.py

from ..ln_client.client import LightningClient

class TransactionStreamer:
    def __init__(self):
        self.client = LightningClient()

    def stream_payment(self, recipient, amount_per_second, duration):
        # Logic for streaming payments
        pass
