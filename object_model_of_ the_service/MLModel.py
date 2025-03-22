from Observer import Observable
from MLTaskItem import MLTaskItem

class MLModel(Observable):
    __cost_per_result = 0.0

    @property
    def cost_per_result(self) -> float:
        return self.__cost_per_result
    
    @cost_per_result.setter
    def cost_per_result(self, cost: float) -> None:
        if cost<0:
            raise ValueError
        self.__cost_per_result = cost

    def do_result(self, task: MLTaskItem) -> dict:
        raise NotImplementedError
    