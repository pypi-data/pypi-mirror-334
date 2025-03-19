import requests
import logging

# Set up logging to capture errors and important messages
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def imageai(prompt: str, api_key: str, timeout: int = 10):
    """
    Calls the image generation API to create an image based on a prompt.

    :param prompt: The text prompt to generate an image.
    :param api_key: The API key required for authentication.
    :param timeout: Request timeout in seconds (default is 10).
    :return: A dictionary containing either the image URL or an error message.
    """

    # Check if prompt is provided
    if not prompt:
        logging.error("Prompt is missing.")
        return {"error": "prompt_error", "message": "Prompt is required to generate an image."}
    
    # Check if API key is provided
    if not api_key:
        logging.error("API key is missing.")
        return {"error": "missing_apikey", "message": "API key is required."}

    IMAGE_URL = "http://fi4.bot-hosting.net:22869/api/image"  # Image generation API URL
    params = {"prompt": prompt, "key": api_key}

    try:
        # Make the API request
        response = requests.get(IMAGE_URL, params=params, timeout=timeout)
        response.raise_for_status()  # Raise an error for 4xx and 5xx status codes
        
        # Parse JSON response
        data = response.json()
        
        # Check if 'image' key exists in the response data
        if 'image' in data:
            return data  # Return the image data (image URL or base64 image)
        
        # If 'image' key is missing in response, log the issue
        logging.error(f"API response missing 'image' key. Full response: {data}")
        return {"error": "unexpected_api_response", "message": "Unexpected API response. Missing 'image' key."}

    except requests.exceptions.Timeout:
        logging.error("Request timed out.")
        return {"error": "timeout_error", "message": "The request timed out. The API may be down or slow."}

    except requests.exceptions.ConnectionError:
        logging.error("Failed to connect to the API.")
        return {"error": "connection_error", "message": "Failed to connect to the API. Check your internet or the API status."}

    except requests.exceptions.HTTPError as http_err:
        # Handle HTTP errors (e.g., 403, 404)
        if response.status_code == 403:
            logging.error("Forbidden access. HTTP error occurred: 403")
            return {"error": "access_denied", "message": "Access denied. Check your API key or permissions."}
        elif response.status_code == 404:
            logging.error("Not found. HTTP error occurred: 404")
            return {"error": "api_not_found", "message": "API endpoint not found."}
        else:
            logging.error(f"HTTP error occurred: {http_err}")
            return {"error": "http_error", "message": f"HTTP error occurred: {http_err}"}

    except requests.exceptions.RequestException as req_err:
        logging.error(f"General error occurred: {req_err}")
        return {"error": "request_error", "message": "An error occurred while communicating with the API."}

    except ValueError:
        logging.error("Invalid response format from the API.")
        return {"error": "response_format_error", "message": "Invalid response format from the API."}
