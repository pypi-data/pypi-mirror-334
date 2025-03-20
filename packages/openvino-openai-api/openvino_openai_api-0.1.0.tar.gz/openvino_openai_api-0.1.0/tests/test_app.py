import pytest
from fastapi.testclient import TestClient
import json
import os
from unittest.mock import patch, MagicMock

# Mock the OpenVINO GenAI imports and functions
@pytest.fixture
def mock_openvino_genai():
    with patch("openvino_genai.Tokenizer") as mock_tokenizer_class:
        mock_tokenizer = MagicMock()
        mock_tokenizer_class.return_value = mock_tokenizer
        mock_tokenizer.apply_chat_template.return_value = "Mocked template output"
        
        with patch("openvino_genai.LLMPipeline") as mock_pipeline_class:
            mock_pipeline = MagicMock()
            mock_pipeline_class.return_value = mock_pipeline
            mock_pipeline.generate.return_value = "This is a mock response"
            
            yield mock_tokenizer, mock_pipeline

@pytest.fixture
def mock_validate_model_path():
    with patch("openvino_openai_api.utils.validate_model_path") as mock_validate:
        mock_validate.return_value = "/mock/model/path"
        yield mock_validate

@pytest.fixture
def client(mock_openvino_genai, mock_validate_model_path):
    from openvino_openai_api.app import create_app
    app = create_app("/mock/model/path", "CPU")
    return TestClient(app)

def test_chat_completion_endpoint(client):
    """Test the chat completion endpoint with a basic request."""
    response = client.post(
        "/v1/chat/completions",
        json={
            "model": "test-model",
            "messages": [
                {"role": "user", "content": "Hello"}
            ],
            "max_tokens": 100
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert "id" in data
    assert data["object"] == "chat.completion"
    assert data["model"] == "test-model"
    assert len(data["choices"]) == 1
    assert data["choices"][0]["message"]["role"] == "assistant"
    assert data["choices"][0]["message"]["content"] == "This is a mock response"
    assert "usage" in data
