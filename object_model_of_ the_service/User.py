from Auth import Auth


class User(Auth):

    def __init__(self, id: int) -> None:
        super(User, self).__init__()
        self.__id = id
        self.__email = None
        self.__first_name = None
        self.__last_name = None
        self.__password = None
        self.__loyalty = 1.0
        
        self.__is_auth = False
        self.__is_admin = False
    
    @property
    def id(self) -> int:
        return self.__id
    

    @property
    def loyalty(self) -> float:
        return self.__loyalty
    
    @loyalty.setter
    def loyalty(self, loyalty: float) -> None:
        if loyalty<=0:
            raise ValueError
        self.loyalty = loyalty



    @property
    def email(self) -> str:
        return self.__email
    
    @email.setter
    def email(self, email:str) -> None:
        pass #check email


    @property
    def first_name(self) -> str:
        return self.__first_name
    
    @first_name.setter
    def first_name(self, first_name:str) -> None:
        pass #check first_name


    @property
    def last_name(self) -> str:
        return self.__last_name
    
    @first_name.setter
    def last_name(self, last_name:str) -> None:
        pass #check last_name


    @property
    def password(self) -> str:
        return self.__password
    
    @password.setter
    def password(self, password: str) -> None:
        self.__password = self.get_password_hash(password)

    @property
    def is_admin(self) -> bool:
        return self.__is_admin
    
    @property
    def is_auth(self) -> bool:
        return self.__is_auth

    def login(self, email: str, password: str) -> object:
        pass
        return self if self.is_auth else None
    
    def logout(self) -> dict:
        return {'message': 'success'} if self.is_auth else {'message': 'fail'}
    
    def registration(self, email: str, first_name: str, last_name: str, password: str) -> object:
        pass
        return self if self.is_auth else None



if __name__=='__main__':
    a = User(1)
    a.loyalty = -3.0
    a.password = 'test'
    print(a.password, a.is_auth)
    

    

