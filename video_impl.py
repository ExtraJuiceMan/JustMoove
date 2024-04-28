from abc import abstractmethod
from typing import Optional

from cv2 import VideoCapture
from numpy import ndarray

class VideoFramesBase:
    @abstractmethod
    def is_open(self) -> bool:
        pass

    @abstractmethod
    def read_frame(self) -> Optional[ndarray]:
        pass
 
class CV2VideoFrames(VideoFramesBase):
    def __init__(self, camera_capture: VideoCapture):
        self.camera_capture = camera_capture

    def is_open(self) -> bool:
        return self.camera_capture.isOpened()
    
    def read_frame(self) -> Optional[ndarray]:
        success, frame = self.camera_capture.read()

        if not success:
            return None

        return frame