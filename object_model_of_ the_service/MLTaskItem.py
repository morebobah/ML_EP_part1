from datetime import datetime
from Items import Item

class MLTaskItem(Item):
    def __init__(self, image: object) -> None:
        super(MLTaskItem, self).__init__(image)
    
    