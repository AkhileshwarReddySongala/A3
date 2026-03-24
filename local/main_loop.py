import cv2
import time
import sys
import os
from dotenv import load_dotenv

# Add project root to path to allow imports from shared
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from local.vision.sfd_logic import SteadyFrameDetector
from local.vision.preprocessing import FrameProcessor
from local.inference.router import HybridInferenceRouter
from shared.utils.voice_utils import VoiceController

load_dotenv()

class A3System:
    def __init__(self):
        print("--- Initializing A3: AI Assembly Assistant ---")
        self.detector = SteadyFrameDetector(threshold=10000, stability_frames=10)
        self.processor = FrameProcessor()
        self.router = HybridInferenceRouter()
        self.voice = VoiceController()
        
        self.cap = cv2.VideoCapture(0)
        self.is_running = False
        self.thinking = False

    def run(self):
        self.is_running = True
        self.voice.start_listening()
        self.voice.speak("A3 system is online. I'm watching your workspace.")

        print("Press 'q' to quit.")
        
        while self.is_running:
            ret, frame = self.cap.read()
            if not ret:
                print("Failed to grab frame.")
                break

            # 1. SEEING: Check for steady frame
            # We only trigger inference if not already thinking
            if not self.thinking:
                triggered = self.detector.is_frame_steady(frame)
                
                if triggered:
                    print("\n[EVENT] Scene stabilized. Starting THINKING phase...")
                    self.thinking = True
                    self.process_inference(frame)

            # 2. LISTENING: Check for voice commands
            command = self.voice.get_command()
            if command:
                self.handle_command(command)

            # 3. UI FEEDBACK
            self.update_ui(frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.is_running = False

        self.cleanup()

    def process_inference(self, frame):
        """
        Handles the 'Thinking' part of the loop in a non-blocking way (simple version).
        For a production version, this would be in a separate thread/process.
        """
        # Visual/Audio Pulse
        self.voice.speak("Analyzing your progress...")
        
        # Preprocess and Encode
        image_b64 = self.processor.encode_to_base64(frame)
        
        # Multimodal Reasoning
        prompt = "You are an assembly assistant. Look at the workspace and provide a one-sentence instruction for the next step. If the user is doing great, say 'Looks good, continue to the next part'."
        messages = [{"role": "user", "content": prompt}]
        
        try:
            # Note: This is currently a blocking call in the main loop.
            # In Phase 6, we will move this to a background thread to keep 30FPS UI.
            response, source = self.router.get_inference(messages, image_b64=image_b64)
            
            # 4. SPEAKING
            print(f"[RESULT] ({source}): {response}")
            self.voice.speak(response)
            
        except Exception as e:
            print(f"Inference error: {e}")
            self.voice.speak("I encountered an error while thinking.")
        
        finally:
            self.thinking = False

    def handle_command(self, command):
        if command == "NEXT":
            self.voice.speak("Moving to the next step.")
            # Logic for manual state transition would go here
        elif command == "REPEAT":
            self.voice.speak("Repeating the last instruction.")
        elif command == "STOP":
            self.voice.speak("Paused.")

    def update_ui(self, frame):
        status_color = (0, 255, 0) if self.detector.motion_counter >= self.detector.stability_frames else (0, 0, 255)
        status_text = f"STABLE: {self.detector.motion_counter}"
        
        if self.thinking:
            status_text = "THINKING..."
            status_color = (255, 0, 0)

        cv2.putText(frame, status_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, status_color, 2)
        cv2.imshow('A3 AI Assembly Assistant', frame)

    def cleanup(self):
        self.is_running = False
        self.voice.stop()
        self.cap.release()
        cv2.destroyAllWindows()
        print("--- A3 System Shutdown ---")

if __name__ == "__main__":
    a3 = A3System()
    try:
        a3.run()
    except KeyboardInterrupt:
        a3.cleanup()
