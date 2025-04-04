from abc import ABCMeta, abstractmethod

class Observer(metaclass=ABCMeta):
 
    @abstractmethod
    def event(self, message: str) -> None:
        pass
    
class Observable(metaclass=ABCMeta):

    def __init__(self) -> None:
        self.observers = []

    def register(self, observer: Observer) -> None:
        self.observers.append(observer)

    def notify_observers(self, message: object) -> None:
        for observer in self.observers:
            observer.event(message)