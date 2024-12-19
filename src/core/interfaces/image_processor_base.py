from abc import ABC,abstractmethod
from typing import Dict, Any

class ImageProcessor(ABC):
    def __init__(self,config_obj):
        self.config_obj = config_obj

    @abstractmethod
    def process(self,image_array,**kwargs)->Dict[Any,Any]:
        pass



