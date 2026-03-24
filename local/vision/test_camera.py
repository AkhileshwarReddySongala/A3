import cv2
import torch
import sys

def check_gpu():
    print("--- GPU Validation ---")
    if torch.cuda.is_available():
        print(f"CUDA is available! Using GPU: {torch.cuda.get_device_name(0)}")
        return True
    else:
        print("CUDA is NOT available. Falling back to CPU.")
        return False

def test_camera():
    print("\n--- Camera Input Pipeline Validation ---")
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open camera (ID 0).")
        return False
    
    print("Camera (ID 0) opened successfully. Press 'q' to quit.")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture frame.")
            break
            
        cv2.imshow('A3 Camera Test', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    cap.release()
    cv2.destroyAllWindows()
    print("Camera test completed.")
    return True

if __name__ == "__main__":
    gpu_ok = check_gpu()
    # Note: Headless environments or those without window managers will fail here.
    # We provide a basic check first.
    try:
        test_camera()
    except Exception as e:
        print(f"Camera test failed or skipped: {e}")
