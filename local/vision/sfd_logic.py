import cv2
import numpy as np
import time

class SteadyFrameDetector:
    def __init__(self, threshold=5000, stability_frames=15, skip_frames=2):
        """
        Steady-Frame Detection (SFD) to optimize VLM inference.
        
        :param threshold: Pixel difference threshold to consider 'motion'.
        :param stability_frames: Number of consecutive frames with NO motion to trigger 'steady'.
        :param skip_frames: Number of frames to skip between checks to reduce CPU load.
        """
        self.threshold = threshold
        self.stability_frames = stability_frames
        self.skip_frames = skip_frames
        
        self.prev_frame = None
        self.motion_counter = 0
        self.frame_count = 0
        self.is_steady = False

    def is_frame_steady(self, frame):
        self.frame_count += 1
        if self.frame_count % self.skip_frames != 0:
            return False

        # Preprocess frame for motion detection (grayscale + blur)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        if self.prev_frame is None:
            self.prev_frame = gray
            return False

        # Calculate absolute difference between current and previous frame
        frame_delta = cv2.absdiff(self.prev_frame, gray)
        thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
        
        # Dilate the thresholded image to fill in holes
        thresh = cv2.dilate(thresh, None, iterations=2)
        motion_score = np.sum(thresh)

        self.prev_frame = gray

        # Logic: If motion is below threshold, increment stability counter
        if motion_score < self.threshold:
            self.motion_counter += 1
        else:
            self.motion_counter = 0
            self.is_steady = False

        # If we have reached the stability requirement, mark as steady
        if self.motion_counter >= self.stability_frames:
            if not self.is_steady:
                self.is_steady = True
                return True # Trigger!
            
        return False

def run_sfd_demo():
    print("Starting Steady-Frame Detection Demo...")
    cap = cv2.VideoCapture(0)
    detector = SteadyFrameDetector(threshold=10000, stability_frames=10)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        triggered = detector.is_frame_steady(frame)
        
        # UI Feedback
        status_color = (0, 255, 0) if detector.motion_counter >= detector.stability_frames else (0, 0, 255)
        status_text = f"STABLE: {detector.motion_counter}"
        
        cv2.putText(frame, status_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, status_color, 2)
        
        if triggered:
            cv2.putText(frame, "TRIGGER INFERENCE!", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)
            print(f"[{time.strftime('%H:%M:%S')}] Scene Stabilized. Ready for Thinking (VLM).")

        cv2.imshow('A3 SFD Test', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_sfd_demo()
