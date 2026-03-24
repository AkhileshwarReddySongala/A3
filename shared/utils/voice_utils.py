import pyttsx3
import speech_recognition as sr
import threading
import queue
import time

class VoiceController:
    def __init__(self):
        """
        Voice Controller for A3: Handles "Speaking" (TTS) and "Listening" (STT).
        Supports interruptible speech and basic assembly commands.
        """
        # TTS Setup
        self.tts_engine = pyttsx3.init()
        self.tts_engine.setProperty('rate', 175) # Comfortable reading speed
        self.is_speaking = False
        
        # STT Setup
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.command_queue = queue.Queue()
        
        # Control flags
        self.stop_listening = None
        self.active = False

    def speak(self, text):
        """
        Speaks the given text in a separate thread.
        """
        print(f"--- AI Speaking: {text} ---")
        
        def _speak():
            self.is_speaking = True
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
            self.is_speaking = False

        # Run TTS in a thread to avoid blocking the main vision/logic loop
        threading.Thread(target=_speak, daemon=True).start()

    def start_listening(self):
        """
        Starts the background listener for voice commands.
        """
        print("--- Voice Command Listener Active ---")
        self.active = True
        
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)

        # Background listening loop
        def callback(recognizer, audio):
            if not self.active:
                return
                
            try:
                # Use Google STT (free, requires internet) or could use local Sphinx
                command = recognizer.recognize_google(audio).lower()
                print(f"--- User Command Detected: '{command}' ---")
                
                # Check for assembly-specific keywords
                if any(k in command for k in ["next", "continue", "go ahead"]):
                    self.command_queue.put("NEXT")
                elif any(k in command for k in ["repeat", "back", "again"]):
                    self.command_queue.put("REPEAT")
                elif any(k in command for k in ["what", "help", "part"]):
                    self.command_queue.put("HELP")
                elif any(k in command for k in ["stop", "wait", "hold"]):
                    self.command_queue.put("STOP")
                    
            except sr.UnknownValueError:
                pass # Silent ignore of noise
            except sr.RequestError as e:
                print(f"Could not request results from STT service; {e}")

        self.stop_listening = self.recognizer.listen_in_background(self.microphone, callback)

    def get_command(self):
        """
        Pops the latest command from the queue.
        """
        try:
            return self.command_queue.get_nowait()
        except queue.Empty:
            return None

    def stop(self):
        """
        Stops the listener.
        """
        self.active = False
        if self.stop_listening:
            self.stop_listening(wait_for_stop=False)
        print("--- Voice Controller Stopped ---")

def test_voice():
    vc = VoiceController()
    vc.speak("System check. I am ready to assist with your assembly. Try saying 'Next' or 'Repeat'.")
    
    vc.start_listening()
    
    try:
        print("Listening for 15 seconds (Try saying 'Next' or 'Repeat')...")
        end_time = time.time() + 15
        while time.time() < end_time:
            cmd = vc.get_command()
            if cmd:
                print(f"PROCESSED COMMAND: {cmd}")
                vc.speak(f"Processing {cmd} command.")
            time.sleep(0.1)
    finally:
        vc.stop()

if __name__ == "__main__":
    test_voice()
