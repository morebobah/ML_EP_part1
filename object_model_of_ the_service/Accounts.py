from Observer import Observable
from User import User
from PayItem import PayItem

class Accounts(Observable):
    def get_balance(self, u: User) -> float:
        current_user_balance = 0.0
        
        return current_user_balance
    
    def add_payment(self, u: User, pay: float) -> float:
        #some account actions
        current_user_balance = self.get_balance(User)
        self.notify_observers(PayItem)
        return current_user_balance
    
    def spend_payment(self, u: User, pay: float) -> float:
        current_user_balance = self.get_balance(User)
        if current_user_balance < pay:
            raise ValueError
        
        #some account actions
        self.notify_observers(PayItem)
        return current_user_balance
       
    