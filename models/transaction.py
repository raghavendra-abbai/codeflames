class Transaction:
    def __init__(self, product_id, sender, receiver, price):
        self.product_id = product_id
        self.sender = sender
        self.receiver = receiver
        self.price = price