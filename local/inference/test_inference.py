import litellm
import os
from dotenv import load_dotenv

# Load environment variables (useful for API keys if needed)
load_dotenv()

def test_local_inference():
    print("--- Local Inference Validation (LM Studio) ---")
    
    # Configuration for LM Studio (usually running on localhost:1234)
    # The 'model' name is whatever is loaded in LM Studio, or can be a generic one.
    custom_llm_config = {
        "model": "openai/local-model", # LiteLLM uses 'openai/' prefix for local OpenAI-compatible APIs
        "api_base": "http://localhost:1234/v1",
        "api_key": "not-needed"
    }

    try:
        print(f"Attempting to connect to LM Studio at {custom_llm_config['api_base']}...")
        
        # Text Input Test
        response = litellm.completion(
            model=custom_llm_config["model"],
            messages=[{"role": "user", "content": "Hello, A3 system check."}],
            api_base=custom_llm_config["api_base"],
            api_key=custom_llm_config["api_key"]
        )
        print("\nText Inference Result:")
        print(response.choices[0].message.content)

        # Note: Vision testing requires base64 encoded images. 
        # For a full test, a real base64 string or file path would be needed.
        print("\nNote: Vision (Qwen3-VL) validation requires an active model with vision support.")
        print("To test vision, ensure 'Qwen3-VL-4B' is loaded in LM Studio and provide a base64 image.")

    except Exception as e:
        print(f"Inference test failed: {e}")
        print("\nTroubleshooting Tips:")
        print("1. Ensure LM Studio is running and the 'Server' tab is active (Start Server).")
        print("2. Confirm the model (e.g., Qwen3-VL-4B) is loaded.")
        print("3. Check the default port (usually 1234).")

if __name__ == "__main__":
    test_local_inference()
