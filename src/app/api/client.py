import json
import requests

def prepare_payload(file_path: str, metadata: dict):
    """Prepare the payload for the POST request."""
    # Reading the file and setting up form data
    with open(file_path, 'rb') as fp:
        file_content = fp.read()

    file = (file_path, file_content , 'image/jpeg')
    files = {
        'file': file,
        'metadata': (None, json.dumps(metadata), 'application/json')
    }
    return files

def send_post_request(url: str, files: dict, headers: dict):
    """Send a POST request to the given URL."""
    try:
        response = requests.post(url, files=files, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def main():
    """Main function to execute the POST request."""
    server_address = "http://0.0.0.0:8000"
    endpoint = "/v2/image_insight/extract"
    # URL and Headers
    url = f'{server_address}{endpoint}'
    headers = {
        'accept': 'application/json'
    }

    # Payload setup
    file_path = 'data/test/images/biryani.jpg'
    metadata = {"labels": ["biryani", "cake", "other food"]}

    # Prepare the payload
    files = prepare_payload(file_path, metadata)

    # Send POST request
    response = send_post_request(url, files, headers=headers)

    # Output response
    print(response)

if __name__ == "__main__":
    main()
