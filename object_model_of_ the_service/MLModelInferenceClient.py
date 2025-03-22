from transformers import AutoProcessor, AutoModelForImageTextToText
from MLModel import MLModel
from MLTaskItem import MLTaskItem

class MLModelInferenceClient(MLModel):
    def do_result(self, task: MLTaskItem) -> dict:
        pass #main work, proccessing with ML task
        result_of_ml_model_working = {'message': 'success'}
        super().notify_observers(MLTaskItem)
        return result_of_ml_model_working