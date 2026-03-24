import cv2
import base64
import numpy as np
from PIL import Image
import io

class FrameProcessor:
    def __init__(self, target_size=(448, 448)):
        """
        Preprocessor for Qwen3-VL and other Vision-Language Models.
        
        :param target_size: (width, height) to resize the frame. Qwen3 often uses 448x448.
        """
        self.target_size = target_size

    def preprocess_for_vlm(self, frame):
        """
        Resize and convert frame to RGB for VLM processing.
        """
        # OpenCV uses BGR, VLMs expect RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Resize frame
        resized_frame = cv2.resize(rgb_frame, self.target_size, interpolation=cv2.INTER_AREA)
        
        return resized_frame

    def encode_to_base64(self, frame):
        """
        Encodes an OpenCV frame (BGR) to a base64 string for API transmission.
        """
        # Convert to RGB before encoding (standard for web/VLMs)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(rgb_frame)
        
        # Save to bytes buffer
        buffer = io.BytesIO()
        pil_img.save(buffer, format="JPEG") # JPEG is usually sufficient and smaller
        
        # Encode to base64
        base64_str = base64.b64encode(buffer.getvalue()).decode('utf-8')
        return f"data:image/jpeg;base64,{base64_str}"

def test_preprocessing():
    print("Testing Frame Preprocessing...")
    # Create a dummy frame (black image)
    dummy_frame = np.zeros((720, 1280, 3), dtype=np.uint8)
    processor = FrameProcessor()
    
    # Preprocess
    preprocessed = processor.preprocess_for_vlm(dummy_frame)
    print(f"Original shape: {dummy_frame.shape} -> Preprocessed shape: {preprocessed.shape}")
    
    # Encode
    b64_img = processor.encode_to_base64(dummy_frame)
    print(f"Base64 String (truncated): {b64_img[:50]}...")
    
    if preprocessed.shape == (448, 448, 3) and b64_img.startswith("data:image/jpeg;base64,"):
        print("Preprocessing test PASSED.")
    else:
        print("Preprocessing test FAILED.")

if __name__ == "__main__":
    test_preprocessing()
