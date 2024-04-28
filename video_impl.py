from abc import abstractmethod
from typing import Optional

from cv2 import VideoCapture
import cv2
from numpy import ndarray

from media_library import PosePosition, VideoMetadata, get_video_file_path

class VideoFramesBase:
    @abstractmethod
    def is_open(self) -> bool:
        pass

    @abstractmethod
    def read_frame(self) -> Optional[ndarray]:
        pass

class RecordedCV2VideoFrames(VideoFramesBase):
    def __init__(self, metadata: VideoMetadata):
        self.metadata = metadata
        self.video = cv2.VideoCapture(get_video_file_path(metadata.id))
        self.last_frame = -1

    def is_open(self) -> bool:
        return self.video.isOpened()

    def read_frame(self) -> Optional[ndarray]:
        success, frame = self.video.read()

        if not success:
            return None

        self.last_frame += 1

        return frame

    def last_frame_pose(self) -> list[PosePosition]:
        return self.metadata.positions[self.last_frame]
    
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