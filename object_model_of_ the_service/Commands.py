from User import User

class Commands:
    
    def __init__(self) -> None:
        self.reset_params()
    
    def user_allowed(self, u: User) -> bool:
        raise NotImplementedError
    
    def set_params(self, params: dict) -> None:
        self.__params = {**self.__params, **params}
    
    def reset_params(self) -> None:
        self.__params = []

    def run(self) -> dict:
        raise NotImplementedError

    
if __name__=='__main__':
    c = Commands()