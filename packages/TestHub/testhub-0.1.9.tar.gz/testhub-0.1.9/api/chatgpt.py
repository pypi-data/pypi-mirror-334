import requests
import logging

class TestHubChatGPT:
    BASE_URL = "http://fi4.bot-hosting.net:22869/TestHubChatgptV4"

    @staticmethod
    def chatgpt(msg: str, api_key: str, timeout: int = 10):
        """
        Calls the TestHubChatGPT API to get a response from ChatGPT-4.

        :param msg: The message to send to ChatGPT.
        :param api_key: The API key required for authentication.
        :param timeout: Request timeout in seconds (default: 10).
        :return: A dictionary containing the API response or an error message.
        """
        if not msg:
            return {"error": "Message is required."}
        if not api_key:
            return {"error": "API key is required."}

        params = {"msg": msg, "key": api_key}

        try:
            # Make the request to the API
            response = requests.get(TestHubChatGPT.BASE_URL, params=params, timeout=timeout)

            # Handle HTTP status codes
            if response.status_code == 403:
                return {"error": "Access forbidden. Please check your API key or permissions."}
            elif response.status_code == 404:
                return {"error": "API endpoint not found. Please check the URL."}
            elif response.status_code >= 500:
                return {"error": f"Server error occurred. Status code: {response.status_code}"}

            # Raise for any status code that isn't 2xx (success)
            response.raise_for_status()

            # Check if the response has the expected key 'chat'
            json_response = response.json()
            if 'chat' in json_response:
                return {"chat": json_response['chat']}
            else:
                return {"error": "Invalid response format. 'chat' key missing."}

        except requests.exceptions.Timeout:
            return {"error": "The request timed out. The API may be down or slow."}

        except requests.exceptions.ConnectionError:
            return {"error": "Failed to connect to the API. Check your internet or the API status."}

        except requests.exceptions.RequestException as req_err:
            return {"error": f"An error occurred: {req_err}"}

        except ValueError:
            return {"error": "Invalid response format from the API."}
