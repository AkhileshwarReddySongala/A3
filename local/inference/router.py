import os
import litellm
import torch
import time
from dotenv import load_dotenv

load_dotenv()

class HybridInferenceRouter:
    def __init__(self):
        """
        Inference Router for A3: Manages Local (Qwen3) vs Cloud (Gemini) failover.
        """
        self.local_base_url = os.getenv("LM_STUDIO_BASE_URL", "http://localhost:1234/v1")
        self.local_model = os.getenv("LOCAL_MODEL_NAME", "openai/local-model")
        self.cloud_model = os.getenv("GEMINI_MODEL_NAME", "gemini/gemini-1.5-flash-latest")
        
        # Ensure cloud model has provider prefix for LiteLLM
        if "gemini" in self.cloud_model.lower() and "/" not in self.cloud_model:
            self.cloud_model = f"gemini/{self.cloud_model}"
        self.vram_threshold = float(os.getenv("VRAM_THRESHOLD_PERCENT", "0.85"))
        self.max_vram = float(os.getenv("MAX_VRAM_GB", "6.0"))

    def check_vram_usage(self):
        """
        Checks current GPU memory usage (NVIDIA only).
        """
        if not torch.cuda.is_available():
            return 1.0 # Force Cloud if no CUDA
            
        # Get free and total memory in bytes
        free_mem, total_mem = torch.cuda.mem_get_info()
        used_mem_gb = (total_mem - free_mem) / (1024**3)
        total_mem_gb = total_mem / (1024**3)
        
        usage_percent = (total_mem - free_mem) / total_mem
        
        print(f"--- Memory Monitor: {used_mem_gb:.2f}GB / {total_mem_gb:.2f}GB Used ({usage_percent*100:.1f}%) ---")
        return usage_percent

    def get_inference(self, messages, image_b64=None):
        """
        Routes the request to Local or Cloud based on health and memory.
        """
        vram_usage = self.check_vram_usage()
        use_cloud = vram_usage > self.vram_threshold
        
        # Build message payload for LiteLLM (Vision-Language)
        content = []
        for msg in messages:
            if isinstance(msg['content'], str):
                content.append({"type": "text", "text": msg['content']})
        
        if image_b64:
            # Add image to the last user message if provided
            content.append({"type": "image_url", "image_url": {"url": image_b64}})

        if not use_cloud:
            try:
                print(f"--- Routing to LOCAL Inference ({self.local_model}) ---")
                start_time = time.time()
                response = litellm.completion(
                    model=self.local_model,
                    messages=[{"role": "user", "content": content}],
                    api_base=self.local_base_url,
                    timeout=10 # Short timeout for local to trigger failover
                )
                print(f"Local Inference Latency: {time.time() - start_time:.2f}s")
                return response.choices[0].message.content, "local"
                
            except Exception as e:
                print(f"Local Inference Failed: {e}. Falling back to Cloud...")
                use_cloud = True

        if use_cloud:
            print(f"--- Routing to CLOUD Inference ({self.cloud_model}) ---")
            start_time = time.time()
            # Note: Ensure GEMINI_API_KEY is in your .env
            response = litellm.completion(
                model=self.cloud_model,
                messages=[{"role": "user", "content": content}],
            )
            print(f"Cloud Inference Latency: {time.time() - start_time:.2f}s")
            return response.choices[0].message.content, "cloud"

def test_router():
    router = HybridInferenceRouter()
    
    # Test text-only request
    messages = [{"role": "user", "content": "System Check: Are you online?"}]
    response, source = router.get_inference(messages)
    print(f"Response from {source}: {response}")

if __name__ == "__main__":
    test_router()
