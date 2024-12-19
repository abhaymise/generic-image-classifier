from typing import Dict, Any

from src.core.interfaces.image_processor_base import ImageProcessor
from src.core.ml.classifier import ZeroShotClassifier

class ClassifierProcessor(ImageProcessor):
    def __init__(self,config=None):
        self.config_obj = config
        self.image_processor = ZeroShotClassifier()


    def process(self,image_array,**kwargs) ->Dict[Any,Any]:
        labels = kwargs.get('labels')
        self.image_processor.set_classes(labels)
        image_insight = self.image_processor.classify_image(image_array)
        return image_insight

class AppFacade:
    def __init__(self):
        self.config = None
        self.processor = ClassifierProcessor(self.config)

    def process_image(self,image_array,**kwargs) -> Dict[Any,Any]:
        image_height,image_width = image_array.shape[:2]
        image_insight = self.processor.process(image_array,**kwargs)
        insight = {
            "image_height":image_height,
            "image_width":image_width,
            "insight" : image_insight
        }
        return insight