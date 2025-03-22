from History import History
from MLModelInferenceClient import MLModel_InferenceClient
from MLTaskItem import MLTaskItem

class HistoryTask(History):

    def __init__(self, mlmodel: MLModel_InferenceClient) -> None:
        mlmodel.register(self)

    def event(self, o: MLTaskItem) -> None:
        pass #add info from MLTaskItem to database

    def get_events(self, filter: dict) -> list:
        pass #extract data from database about MLTasks events with filter dict params
        return [MLTaskItem(), MLTaskItem()] #sample of return values