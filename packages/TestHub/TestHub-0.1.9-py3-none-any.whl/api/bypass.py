import requests
import logging

# Set up basic logging configuration (logs to console)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Bypass:
    BASE_URL = "http://fi4.bot-hosting.net:22869/bypass"

    @staticmethod
    def bypass_url(url: str, api_key: str, timeout: int = 10):
        """
        Calls the bypass API to process a given URL.

        :param url: The URL to bypass.
        :param api_key: The API key required for authentication.
        :param timeout: Request timeout in seconds (default: 10).
        :return: A dictionary containing the API response or an error message.
        """
        # Validate inputs
        if not url:
            logging.error("URL is missing or invalid.")
            return {"error": "link_error", "message": "The URL is required."}
        if not api_key:
            logging.error("API key is missing.")
            return {"error": "missing_apikey", "message": "API key is required."}

        params = {"url": url, "key": api_key}

        try:
            response = requests.get(Bypass.BASE_URL, params=params, timeout=timeout)
            response.raise_for_status()  # Raises an error for 4xx and 5xx status codes
            
            # Check if the 'result' key exists in the response
            data = response.json()
            if 'result' in data:
                return data  # If 'result' exists, return the full response

            # If 'result' does not exist in the response, log and return a general error
            logging.error(f"API response missing 'result' key. Full response: {data}")
            return {"error": "unexpected_api_response", "message": "Unexpected API response. Missing 'result' key."}

        except requests.exceptions.Timeout:
            logging.error("Request timed out.")
            return {"error": "timeout_error", "message": "The request timed out. The API may be down or slow."}

        except requests.exceptions.ConnectionError:
            logging.error("Failed to connect to the API.")
            return {"error": "connection_error", "message": "Failed to connect to the API. Check your internet or the API status."}

        except requests.exceptions.HTTPError as http_err:
            # We can add more specific handling for certain HTTP error codes
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
