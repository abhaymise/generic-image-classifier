from abc import ABC,abstractmethod
from ..models.ml_model import MLModel

class MLModule(ABC):
    model_obj = MLModel()

    @abstractmethod
    def __load_model(self):
        pass

    @abstractmethod
    def __load_labels(self):
        pass

    @property
    def __unload_model(self):
        self.model = None
        self.model_version = None

    @property
    def __unload_labels(self):
        self.labels = None

    @abstractmethod
    def predict(self,input):
        pass

    @abstractmethod
    def predict_batch(self,input):
        pass


    def preprocess(self,input):
        pass

    def postprocess(self,input):
        pass

    def decode_ids(self,input):
        pass




