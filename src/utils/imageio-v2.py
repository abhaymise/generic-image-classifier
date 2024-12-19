import base64
import mimetypes
import os
import logging
import numpy as np
from io import BytesIO
from PIL import Image
import requests


def get_mime_type(file_path):
    """
    Get the MIME type of the image file.
    """
    mime_type, _ = mimetypes.guess_type(file_path)
    return mime_type


def setup_logger():
    """
    Setup logger with the app name from environment variables.
    """
    app_name = os.environ.get("app_name", __file__)
    logger = logging.getLogger(app_name)
    logger.setLevel(logging.INFO)
    return logger


logger = setup_logger()


def image_file_to_bytes(image_path):
    """
    Load an image from a file and convert it to bytes.
    """
    with open(image_path, "rb") as file:
        return file.read()


def image_file_to_base64(image_path):
    """
    Encodes an image file to a base64 string with its MIME type.
    """
    mime_type = get_mime_type(image_path)
    if not mime_type:
        raise ValueError("Unable to determine MIME type for the given file.")

    image_bytes = image_file_to_bytes(image_path)
    base64_encoded = base64.b64encode(image_bytes).decode("utf-8")
    return f"data:{mime_type};base64,{base64_encoded}", mime_type


def image_to_array(image_bytes):
    """
    Convert image bytes to a NumPy array.
    """
    return np.array(Image.open(BytesIO(image_bytes)))


def image_file_to_array(image_path):
    """
    Load an image from a file and convert it to a NumPy array.
    """
    return image_to_array(image_file_to_bytes(image_path))


def image_url_to_bytes(url):
    """
    Load an image from a URL and convert it to bytes.
    """
    response = requests.get(url)
    return response.content, response.headers['Content-Type']


def image_url_to_base64(url):
    """
    Load an image from a URL and convert it to a base64 string.
    """
    image_bytes, mime_type = image_url_to_bytes(url)
    base64_encoded = base64.b64encode(image_bytes).decode("utf-8")
    return f"data:{mime_type};base64,{base64_encoded}", mime_type


def image_url_to_array(url):
    """
    Load an image from a URL and convert it to a NumPy array.
    """
    image_bytes, _ = image_url_to_bytes(url)
    return image_to_array(image_bytes)


def base64_to_bytes(base64_str):
    """
    Convert a base64 string to bytes.
    """
    if base64_str.startswith("data:"):
        base64_data = base64_str.split(",", 1)[1]
    else:
        base64_data = base64_str
    return base64.b64decode(base64_data)


def image_base64_to_array(base64_str):
    """
    Decodes a base64 string into a NumPy array.
    """
    return image_to_array(base64_to_bytes(base64_str))


def image_array_to_base64(image_array, mime_type="image/jpeg"):
    """
    Encodes an image array to a base64 string with the specified MIME type.
    """
    image = Image.fromarray(image_array)
    with BytesIO() as buffer:
        image.save(buffer, format=mime_type.split("/")[1].upper())
        base64_data = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return f"data:{mime_type};base64,{base64_data}"


def image_array_to_bytes(image_array, mime_type="image/jpeg"):
    """
    Convert a NumPy image array to bytes.
    """
    image = Image.fromarray(image_array)
    with BytesIO() as buffer:
        image.save(buffer, format=mime_type.split("/")[1].upper())
        return buffer.getvalue()


def image_input_to_array(input_data):
    """
    Convert input data (URL, Base64, bytes, file path) to a NumPy image array.
    """
    if isinstance(input_data, np.ndarray):
        logger.info("Data is already a NumPy array.")
        return input_data

    if isinstance(input_data, bytes):
        logger.info("Data is bytes, decoding...")
        return image_to_array(input_data)

    if isinstance(input_data, str):
        if input_data.startswith("http://") or input_data.startswith("https://"):
            logger.info("Data is a URL, decoding...")
            return image_url_to_array(input_data)

        if os.path.exists(input_data):
            logger.info("Data is a file path, decoding...")
            return image_file_to_array(input_data)

        logger.info("Data is a Base64 string, decoding...")
        return image_base64_to_array(input_data)

    raise TypeError("Unsupported input type. Provide a valid file path, URL, Base64 string, or bytes.")
