import base64
import mimetypes
from pathlib import Path
import os
import numpy as np
from PIL import Image
from io import BytesIO
import requests
import logging

def get_mime_type(file_path):
    """
    Get the MIME type of the image file.

    Args:
        file_path (str): Path to the image file.

    Returns:
        str: MIME type of the image.
    """
    mime_type, _ = mimetypes.guess_type(file_path)
    return mime_type


app_name = os.environ.get("app_name", __file__)
logger = logging.getLogger(os.environ.get("app_name", __file__))
logger.setLevel(logging.INFO)


def image_file_to_bytes(image_path):
    """
    Load an image from a file and convert it to bytes.

    Args:
        image_path (str): Path to the image file.

    Returns:
        bytes: Image data in bytes.
    """
    with open(image_path, "rb") as file:
        image_bytes = file.read()
    return image_bytes


def image_file_to_base64(image):
    """
    Encodes an image file to a base64 string with its MIME type.

    Args:
        image (str): Path to the image file.

    Returns:
        tuple: A tuple containing:
            - str: The base64-encoded image string.
            - str: The MIME type of the image.
            :param mime_type:
    """
    # Get the MIME type based on the file extension
    mime_type, _ = mimetypes.guess_type(image)
    if not mime_type:
        raise ValueError("Unable to determine MIME type for the given file.")

    # Read the file in binary mode and encode it to base64
    image_bytes = image_file_to_bytes(image)
    base64_encoded = base64.b64encode(image_bytes).decode("utf-8")

    # Construct the base64 string with MIME type prefix
    base64_string = f"data:{mime_type};base64,{base64_encoded}"
    return base64_string, mime_type


def image_file_to_array(image_path):
    """
    Load an image from a file and convert it to a NumPy array.

    Args:
        image_path (str): Path to the image file.

    Returns:
        numpy.ndarray: Image as a NumPy array.
    """
    image = Image.open(image_path)
    return np.array(image)


def image_url_to_array(url):
    """
    Load an image from a URL and convert it to a NumPy array.

    Args:
        url (str): URL of the image to load.

    Returns:
        numpy.ndarray: Image as a NumPy array.
    """
    response = requests.get(url)
    image = Image.open(BytesIO(response.content))
    return np.array(image)


def image_url_to_bytes(url):
    """
    Load an image from a URL and convert it to bytes.

    Args:
        url (str): URL of the image to load.

    Returns:
        bytes: Image data in bytes.
    """
    response = requests.get(url)
    return response.content, response.headers['Content-Type']


def image_url_to_base64(url):
    """
    Load an image from a URL and convert it to a base64 string.

    Args:
        url (str): URL of the image to load.

    Returns:
        str: Base64-encoded image string.
    """
    # response = requests.get(url)
    image_bytes, mime_type = image_url_to_bytes(url)
    base64_encoded = base64.b64encode(image_bytes).decode("utf-8")
    return f"data:{mime_type};base64,{base64_encoded}"


def image_bytes_to_array(image_bytes):
    """
    Load an image from bytes and convert it to a NumPy array.

    Args:
        image_bytes (bytes): Image data in bytes.

    Returns:
        numpy.ndarray: Image as a NumPy array.
    """
    image = Image.open(BytesIO(image_bytes))
    return np.array(image)


def base64_to_bytes(base64_str):
    """
    Convert a base64 string to bytes.

    Args:
        base64_str (str): Base64-encoded string.

    Returns:
        bytes: Decoded byte data.
    """
    # Check for MIME type prefix
    if base64_str.startswith("data:"):
        mime_type, base64_data = base64_str.split(";", 1)
        mime_type = mime_type.split(":")[1]
        base64_data = base64_data.split(",")[1]  # Extract the actual base64 data
    else:
        mime_type = "unknown"
        base64_data = base64_str
    # Decode the base64 string into bytes
    image_bytes = base64.b64decode(base64_data)
    return image_bytes, mime_type


def image_base64_to_array(base64_str):
    """
    Decodes a base64 string into a NumPy array and extracts the MIME type.

    Args:
        base64_str (str): Base64 string of the image. Can include a MIME type prefix.

    Returns:
        tuple: A tuple containing:
            - numpy.ndarray: The decoded image as a NumPy array.
            - str: The MIME type of the image.
    """

    image_bytes, mime_type = base64_to_bytes(base64_str)
    # Convert bytes to an image and then to a NumPy array
    image = image_bytes_to_array(image_bytes)
    image_array = np.array(image)
    return image_array, mime_type


def image_array_to_base64(image_array, mime_type="image/jpeg"):
    """
    Encodes an image array to a base64 string with the specified MIME type.

    Args:
        image_array (numpy.ndarray): The input image as a numpy array.
        mime_type (str): MIME type of the image (e.g., 'image/png', 'image/jpeg').

    Returns:
        str: Base64-encoded string with MIME type prepended.
    """
    # Convert the numpy array back to an image
    image = Image.fromarray(image_array)
    with BytesIO() as buffer:
        image.save(buffer, format=mime_type.split("/")[1].upper())
        base64_data = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return f"data:{mime_type};base64,{base64_data}"


def image_array_to_bytes(img_array, mime_type="image/jpeg"):
    """
    Convert a NumPy image array to bytes.

    Args:
        img_array (numpy.ndarray): Image represented as a NumPy array.
        mime_type (str): MIME type of the image (default: "image/jpeg").

    Returns:
        bytes: Byte data of the image.
    """
    img = Image.fromarray(img_array)
    with BytesIO() as buffer:
        img.save(buffer, format=mime_type.split("/")[1].upper())
        byte_data = buffer.getvalue()
    return byte_data


def image_input_to_array(input_data, mime_type=None):
    """
    Convert input data (URL, Base64, bytes) to a NumPy image array.

    Args:
        input_data: The input image data, which can be a URL, Base64 string, or bytes.
        mime_type (str, optional): MIME type of the input data. Defaults to None.

    Returns:
        tuple: A tuple containing (numpy.ndarray, str) where the first element is the image array and the second is the MIME type.
    """
    image_array = np.empty(0)
    inferred_mime = "image/jpeg"
    if isinstance(input_data, np.ndarray):
        logger.info(f"the data is a array, not decoding it ...")
        image_array = input_data

    elif isinstance(input_data, bytes):
        logger.info(f"the data is a bytes, decoding it ...")
        image_array = image_bytes_to_array(input_data)
        inferred_mime = mime_type if mime_type else "image/jpeg"

    elif isinstance(input_data, str):
        if input_data.startswith(("http://","https://")) :
            logger.info(f"the data is a url, decoding it ...")
            image_array = image_url_to_array(input_data)

        elif isinstance(input_data, str):
            # Check if the string is a valid file path
            if os.path.exists(input_data):
                logger.info(f"the data is a a file, decoding it ...")
                image_array = image_file_to_array(input_data)
            else:
                logger.info(f"trying through base64 string, decoding it ...")
                # Check if the string is a base64-encoded image
                try:
                    image_array, inferred_mime = image_base64_to_array(input_data)
                except (base64.binascii.Error, ValueError):
                    logger.info(f"base64 string decoding failed")
        else:
            raise TypeError("Unsupported input type. Provide a valid file path, URL, Base64 string, or bytes.")
    return image_array, inferred_mime

if __name__ == "__main__":
    image_path = "/Users/abhaykumar/Documents/datasets/food/images/test/biryani/biryani.jpg"
    image_url = "https://www.freshtohome.com/blog/wp-content/uploads/2024/08/Biryani.jpeg"
    image_base64str = "data:image/jpeg;base64,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"
    print(f"image path to array")
    img_array, inferred_mime = image_input_to_array(image_path)
    print(img_array.shape)