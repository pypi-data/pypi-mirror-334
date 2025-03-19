# TestHub

TestHub is a Python library that allows you to interact with various APIs, including bypassing URLs, ChatGPT API, and more. Join our discord
https://discord.gg/3wKTDFMwvN
## Features

- **Bypass URL**
- **ChatGPT** (based on GPT-4)
- **Image Generation**



Example Code

```py
from TestHub.api.chatgpt import TestHubChatGPT


response = TestHubChatGPT.chatgpt(msg="Hello, how are you?", api_key="TestHub-FqgYrvBnmyLFqqwK1v0LigEu")


if "error" in response:
    print(f"Error: {response['error']}")
else:
    
    print(f"ChatGPT Response: {response['chat']}")




## Installation

You can install TestHub via pip:

```bash
pip install TestHub
