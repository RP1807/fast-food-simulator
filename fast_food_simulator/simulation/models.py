from django.db import models
from uuid import uuid4


class OrderTicket:

    def __init__(self):
        self.id = f"tk_{str(uuid4())[:8]}"

    def __str__(self):
        return self.id


class Customer:

    def __init__(self):
        self.id = f"cust_{str(uuid4())[:8]}"

    def __str__(self):
        return self.id

