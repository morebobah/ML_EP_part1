from services.crud.observer import Observer

class histories(Observer):
    def event(self, o: object):
        raise NotImplementedError
    
    def get_events(self, filter: dict) -> list:
        raise NotImplementedError