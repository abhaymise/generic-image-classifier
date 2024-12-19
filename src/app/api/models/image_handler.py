from datetime import datetime
from typing import Any, List, Dict

from fastapi import Form, UploadFile, File, Body, Header
from pydantic import BaseModel, Field


class Request(BaseModel):
    file: UploadFile = File(None),
    url : str = Form(None),
    base64str : str = Form(None),
    metadata : dict = Body({}),
    # header : Header = Header({})

class Response(BaseModel):
    id : str 
    insight : Dict[Any,Any]
    image_height : int
    image_width : int
    status_code : int
    message : str
    created_at : str = Field(datetime.utcnow().strftime("%Y%m%d::%H%M%S"),description="response creation time")