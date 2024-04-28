from typing import Optional

from skellytracker.trackers.base_tracker.base_tracker import BaseTracker
from scenes.scene import SceneBase
from game_state import GameVideoConfiguration, GameState
import numpy as np
import pygame
import cv2

class PoseFrame:
    def __init__(self, frame: np.ndarray, motion_tracker: BaseTracker):
        self.frame = frame
        self.frame = cv2.rotate(self.frame, cv2.ROTATE_90_COUNTERCLOCKWISE, self.frame)
        self.pose_positions = motion_tracker.process_image(frame)
        self.raw_frame: np.ndarray = motion_tracker.raw_image

    def frame_size(self):
        return self.frame.shape

    def unannotated_surface(self) -> pygame.Surface:
        return pygame.surfarray.make_surface(self.raw_frame)

    def surface(self) -> pygame.Surface:
        return pygame.surfarray.make_surface(self.frame)
    
class GameScene(SceneBase):
    def __init__(self, video_config: GameVideoConfiguration, state: GameState):
        self.video_config = video_config
        self.state = state
        SceneBase.__init__(self)

    def handle_event(self, event: pygame.event.Event):
        pass
    
    def update(self):
        pass
    
    def render(self, screen: pygame.Surface):
        frame_available, camera_frame = self.video_config.camera.read_frame()

        if not frame_available:
            return

        frame_available, video_frame = self.video_config.video.read_frame()

        if not frame_available:
            return

        pose_camera = PoseFrame(camera_frame, self.video_config.motion_tracker)
        pose_video = PoseFrame(video_frame, self.video_config.motion_tracker)

        # Display the frame
        screen.blit(pose_video.surface(), (0, 0))