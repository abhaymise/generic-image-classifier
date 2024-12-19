from typing import Dict, Any

from src.core.interfaces.image_processor_base import ImageProcessor

class SampleImageProcessor(ImageProcessor):
    def __init__(self,config=None):
        self.config_obj = config


    def process(self,image_array,**kwargs) ->Dict[Any,Any]:
        image_height, image_width = image_array.shape[:2]
        insight = {
            "image_height": image_height,
            "image_width": image_width,
            "insight": {},
            "args":kwargs
        }
        return insight

class AppFacade:
    def __init__(self):
        self.config = None
        self.processor = SampleImageProcessor(self.config)

    def process_image(self,image_array,**kwargs) -> Dict[Any,Any]:
        image_insight = self.processor.process(image_array,**kwargs)
        return image_insight