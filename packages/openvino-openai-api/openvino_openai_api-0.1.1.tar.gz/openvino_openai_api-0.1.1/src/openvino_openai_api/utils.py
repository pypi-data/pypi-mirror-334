import os
import json

def validate_model_path(model_path):
    """Validate that the model path exists and contains required files."""
    if not os.path.exists(model_path):
        raise ValueError(f"Model path does not exist: {model_path}")
    
    # Check for required files
    if not os.path.exists(os.path.join(model_path, "openvino_model.bin")):
        raise ValueError("No OpenVINO model available")
    
    if not os.path.exists(os.path.join(model_path, "openvino_tokenizer.bin")):
        raise ValueError("No OpenVINO tokenizer available")
    
    if not os.path.exists(os.path.join(model_path, "openvino_detokenizer.bin")):
        raise ValueError("No OpenVINO detokenizer available")
    
    # Check for tokenizer_config.json and validate chat_template
    tokenizer_config_path = os.path.join(model_path, "tokenizer_config.json")
    if not os.path.exists(tokenizer_config_path):
        raise ValueError("No tokenizer_config.json available")
    
    try:
        with open(tokenizer_config_path, 'r', encoding='utf-8') as f:
            tokenizer_config = json.load(f)
        
        if "chat_template" not in tokenizer_config or not tokenizer_config["chat_template"]:
            raise ValueError("chat_template is missing or empty in tokenizer_config.json")
    except json.JSONDecodeError:
        raise ValueError("tokenizer_config.json is not a valid JSON file")
    except Exception as e:
        raise ValueError(f"Error reading tokenizer_config.json: {str(e)}")
    
    return model_path