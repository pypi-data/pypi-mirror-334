#!/usr/bin/env python3
import sys
import argparse
import uvicorn
from .utils import validate_model_path
from .app import create_app

def main():
    """Entry point for the application script"""
    parser = argparse.ArgumentParser(description="OpenAI Compatible API Server with OpenVINO")
    
    parser.add_argument(
        "--model-path",
        type=str,
        default="SmolLM2-360M-Instruct-openvino-8bit",
        help="Path to the OpenVINO model directory"
    )
    
    parser.add_argument(
        "--device",
        type=str,
        default="GPU",
        choices=["CPU", "GPU"],
        help="Device to run inference on (CPU or GPU)"
    )
    
    parser.add_argument(
        "--host",
        type=str,
        default="127.0.0.1",
        help="Host address to bind the server to"
    )
    
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port to bind the server to"
    )
    
    args = parser.parse_args()
    
    # Validate the model path
    try:
        validate_model_path(args.model_path)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Create the FastAPI app with the configured settings
    app = create_app(args.model_path, args.device)
    
    # Run the server
    uvicorn.run(app, host=args.host, port=args.port)

if __name__ == "__main__":
    main()