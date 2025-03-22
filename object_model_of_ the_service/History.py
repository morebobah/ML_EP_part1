from Observer import Observer

class History(Observer):
    def event(self, o: object):
        raise NotImplementedError
    
    def get_events(self, filter: dict) -> list:
        raise NotImplementedError