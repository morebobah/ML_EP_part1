from Commands import Commands
from User import User
from Accounts import Accounts
from MLModelInferenceClient import MLModelInferenceClient

class Registration(Commands):
    def user_allowed(self, u: User) -> bool:
        return True #always True
    
    def run(self) -> dict:
        # prepare data and call User.Registration method
        return {'message': 'success'}



class Login(Commands):
    def user_allowed(self, u: User) -> bool:
        return True #always True
    
    def run(self) -> dict:
        # prepare data and call User.Login method
        return {'message': 'success'}



class Logout(Commands):
    def user_allowed(self, u: User) -> bool:
        return True #always True
    
    def run(self) -> dict:
        # just call User.Login method
        return {'message': 'success'}
    


class SetBalance(Commands):
    def user_allowed(self, u: User) -> bool:
        return True #sometimes True
    
    def run(self) -> dict:
        # prepare data and call Accounts.SetBalance method
        return {'message': 'success'}



class CreateTask(Commands):
    def user_allowed(self, u: User) -> bool:
        return True #sometimes True
    
    def run(self) -> dict:
        # prepare data and pack it to MLTaskItem
        return {'message': 'success'}



class RunModel(Commands):
    def user_allowed(self, u: User) -> bool:
        return True #sometimes True
    
    def run(self) -> dict:
        # run MLModel with prepared MLTaskItem
        return {'message': 'success'}



class GetListOfPays(Commands):
    def user_allowed(self, u: User) -> bool:
        return True #sometimes True
    
    def run(self) -> dict:
        # prepare data and run HistoryPay.get_events
        return {'message': 'success', 'result': 'list([PayItem, PayItem])'}



class GetListOfTasks(Commands):
    def user_allowed(self, u: User) -> bool:
        return True #sometimes True
    
    def run(self) -> dict:
        # prepare data and run HistoryTask.get_events
        return {'message': 'success', 'result': 'list([MLTaskItem, MLTAskItem])'}