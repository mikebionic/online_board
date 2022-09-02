import cv2
from document import Scanner

class VideoCamera(object):
    def __init__(self):
        # Open a camera
        self.cap = cv2.VideoCapture(2)
      
        # Initialize video recording environment
        self.is_record = False
        self.out = None
        self.transformed_frame = None

        self.scanner = Scanner()
        self.cached_frame = None
    
    def __del__(self):
        self.cap.release()

    def get_video_frame(self):
        ret, frame = self.cap.read()
        if ret:
            frame, _ = self.scanner.detect_edge(frame)
            self.cached_frame = frame
            ret, jpeg = cv2.imencode('.jpg', frame)
            return jpeg.tobytes()
        else:
            return None

    def capture_frame(self):
        ret, frame = self.cap.read()
        if ret:
            _, frame = self.scanner.detect_edge(frame, True)
            ret, jpeg = cv2.imencode('.jpg', frame)
            self.transformed_frame = jpeg.tobytes()
        else:
            return None

    def get_cached_frame(self):
        return self.cached_frame

    def get_image_frame(self):
        return self.transformed_frame

