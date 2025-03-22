from History import History
from Accounts import Accounts
from PayItem import PayItem

class HistoryPay(History):

    def __init__(self, account: Accounts) -> None:
        account.register(self)

    def event(self, o: PayItem) -> None:
        pass #add info from PayItem to database

    def get_events(self, filter: dict) -> list:
        pass #extract data from database about Payment events with filter dict params
        return [PayItem(), PayItem()] #sample of return values