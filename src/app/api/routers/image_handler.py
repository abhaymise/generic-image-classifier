import logging
import os
import uuid

from fastapi import APIRouter, Request, status, HTTPException
from fastapi import  File, UploadFile, Body, Form, Header
import json

from src.app.api.models.image_handler import Response
from src.utils.imageio import image_input_to_array
from src.facade import AppFacade

def setup_logger():
    """
    Setup logger with the app name from environment variables.
    """
    app_name = os.environ.get("app_name", __file__)
    logger = logging.getLogger(app_name)
    logger.setLevel(logging.INFO)
    return logger


logger = setup_logger()

facade = AppFacade()
router = APIRouter(
     prefix="/v2/image_insight",
     tags=["image_insight"]
)



@router.post("/extract", response_description="processes image", status_code=status.HTTP_200_OK)
async def process_image(
        request : Request,
        file: UploadFile = File(None),
        url : str = Form(None),
        base64str : str = Form(None),
        metadata : str = Body({}),
        header = Header(None)
    ):
    """
    ## Overview

    Takes an image in form bytes/image_url/base64 and classifies it in one of the categories specified
    by labels in metadata.


    The classification is generated as insight in form of json.


    for a working script refer to **client.py**

    <hr>

    ## Parameters :
    - file: <Optional>
    - url: <Optional>
    - base64str: <Optional>
    - metadata: dictionary having labels defined
    - header: <Optional>

    - return: json

    ### Metadata should have labels in which you want the image to be classified

    Example :
    to classify an image as `biryani`/`cake`/`other food`
    metadata should be passed as
    ``` json
    {
        "labels" : ["biryani","cake","other food"]
    }
    ```

    ### Sample response :
    ``` json
    {
      "id": "291cc06f-14d1-4e68-81b8-c38a96cc1b17",
      "insight": {
        "prediction": {
          "label": "biryani",
          "confidence": 0.35582542419433594
        },
        "other_predictions": [
          {
            "label": "biryani",
            "confidence": 0.35582542419433594
          },
          {
            "label": "other food",
            "confidence": 0.32970619201660156
          },
          {
            "label": "cake",
            "confidence": 0.3144683241844177
          }
        ],
        "model_name": "openai/clip-vit-base-patch32"
      },
      "image_height": 405,
      "image_width": 540,
      "status_code": 200,
      "message": "success",
      "created_at": "20241219::123844"
    }
    ```
    """
    request_id = str(uuid.uuid4())
    response = {}
    file_name = "image.jpeg"
    inferred_mime = "image/jpeg"
    try:
        if file:
            if file.content_type not in ["image/jpeg", "image/png", "application/pdf"]:
                raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                                    detail="Invalid file type.")

            file_name = file.filename
            inferred_mime  = file.content_type
            content = await file.read()
            image_array, inferred_mime = image_input_to_array(content,inferred_mime)
        elif url:
            content = url
            image_array, _ = image_input_to_array(content)
        elif base64str:
            content = base64str
            image_array, _ = image_input_to_array(content)
        else:
            status_code = status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
            message = "file media not supported"
            raise HTTPException(status_code=status_code,
                                detail=message)

        metadata = json.loads(metadata)
        response = facade.process_image(image_array,**metadata)
        status_code = status.HTTP_200_OK
        message = "success"
    except Exception as e:
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        message = "server error"
        logger.exception(e,exc_info=True)
        raise HTTPException(status_code=status_code,detail=message)
    finally:
        response = {
            "id":request_id,
            **response,
            "status_code":status_code,
            "message":message
        }
        response = Response(**response)
    return response
