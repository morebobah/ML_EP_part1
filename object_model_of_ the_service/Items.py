from datetime import datetime
from User import User

class Item:
    def __init__(self, value: type) -> None:
        self.__id = None
        self.value = type
        self.owner = None
        self.created = datetime.now()
        self.processed = None
        self.result = 'Unknown'
    
    @property
    def id(self) -> int:
        return self.__id
    
    @id.setter
    def id(self, id: int) -> None:
        if id>0:
            self.__id = id