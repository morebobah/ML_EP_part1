from datetime import datetime
from Items import Item

class PayItem(Item):

    def __init__(self, pay: float) -> None:
        super(PayItem, self).__init__(pay)
    