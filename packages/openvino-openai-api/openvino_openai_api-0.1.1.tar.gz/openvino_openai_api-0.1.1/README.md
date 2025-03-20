# OpenVINO OpenAI API

An OpenAI-compatible API server powered by OpenVINO GenAI for efficient inference on Intel hardware.

## Features

- OpenAI API compatibility for easy integration with existing applications
- Powered by OpenVINO for optimized inference on Intel CPUs and GPUs
- Support for both streaming and non-streaming responses
- Simple command-line interface for launching the server

## Installation

```bash
pip install openvino-openai-api
```

## Requirements

- Python 3.11 (due to dependency issues, only python 3.11 is supported)
- OpenVINO GenAI
- FastAPI
- Uvicorn

## Usage

### Starting the server

```bash
# Launch with default settings
openvino-openai-server --model-path /path/to/your/model

# Custom configuration
openvino-openai-server --model-path /path/to/your/model --device CPU --host 0.0.0.0 --port 8000
```

### Sending requests

The API is compatible with OpenAI's chat completions endpoint:

```python
import requests
import json

url = "http://localhost:8000/v1/chat/completions"
headers = {"Content-Type": "application/json"}
data = {
    "model": "local-model",
    "messages": [
        {"role": "user", "content": "Hello, how are you?"}
    ],
    "max_tokens": 500
}

response = requests.post(url, headers=headers, data=json.dumps(data))
print(response.json())
```

### Streaming responses

For streaming responses, set `stream=True` in your request and handle the server-sent events:

```python
import requests
import json

url = "http://localhost:8000/v1/chat/completions"
headers = {"Content-Type": "application/json"}
data = {
    "model": "local-model",
    "messages": [
        {"role": "user", "content": "Tell me a story"}
    ],
    "max_tokens": 500,
    "stream": True
}

response = requests.post(url, headers=headers, data=json.dumps(data), stream=True)
for line in response.iter_lines():
    if line:
        line = line.decode('utf-8')
        if line.startswith('data: ') and not line.endswith('[DONE]'):
            json_str = line[6:]  # Remove 'data: ' prefix
            try:
                chunk = json.loads(json_str)
                content = chunk['choices'][0]['delta'].get('content', '')
                if content:
                    print(content, end='', flush=True)
            except json.JSONDecodeError:
                pass
print()
```

## Model Requirements

The model directory should contain the following files:
- `openvino_model.bin`
- `openvino_tokenizer.bin`
- `openvino_detokenizer.bin`
- `tokenizer_config.json` with a valid `chat_template` defined

## Development

### Setup development environment

```bash
git clone https://github.com/yourusername/openvino-openai-api.git
cd openvino-openai-api
pip install -e ".[dev]"
```

### Running tests

```bash
pytest
```

## License

This project is licensed under the terms of the MIT license.
