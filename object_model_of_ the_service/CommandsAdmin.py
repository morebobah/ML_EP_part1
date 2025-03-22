from Commands import Commands
from User import User
from Accounts import Accounts
from MLModelInferenceClient import MLModelInferenceClient

class CreateUser(Commands):
    def user_allowed(self, u: User) -> bool:
        return u.is_admin
    
    def run(self) -> dict:
        if not self.user_allowed:
            raise PermissionError
        # prepare data and call User.Registration method
        return {'message': 'success', 'result': User}



class GetListOfUsers(Commands):
    def user_allowed(self, u: User) -> bool:
        return u.is_admin
    
    def run(self) -> dict:
        if not self.user_allowed:
            raise PermissionError
        pass
        return {'message': 'success', 'result': '[User, User, User]'}



class UserToAdmin(Commands):
    def user_allowed(self, u: User) -> bool:
        return u.is_admin
    
    def run(self) -> dict:
        if not self.user_allowed:
            raise PermissionError
        pass
        return {'message': 'success'}



class SetUserBalance(Commands):
    def user_allowed(self, u: User) -> bool:
        return u.is_admin
    
    def run(self) -> dict:
        if not self.user_allowed:
            raise PermissionError
        pass
        return {'message': 'success'}



class ResetPassword(Commands):
    def user_allowed(self, u: User) -> bool:
        return u.is_admin
    
    def run(self) -> dict:
        if not self.user_allowed:
            raise PermissionError
        pass
        return {'message': 'success'}