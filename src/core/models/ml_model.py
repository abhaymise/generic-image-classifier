from typing import List, Any
from pydantic import BaseModel


class MLModel(BaseModel):
    model: Any = None
    model_name : str = None
    model_version : float = None
    model_path : str = None
    model_url : str = None
    labels : List = None