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
        self.pose_positions = motion_tracker.process_image(self.frame)
        self.raw_frame: np.ndarray = motion_tracker.raw_image

    def frame_size(self):
        return self.frame.shape

    def unannotated_surface(self) -> pygame.Surface:
        return pygame.surfarray.make_surface(self.raw_frame)

    def surface(self) -> pygame.Surface:
        return pygame.surfarray.make_surface(self.frame)

    def centered_draw_coords(self, screen_dim: tuple[int, int], left: bool) -> tuple[int, int]:
        if left:
            return (screen_dim[0] // 2 - self.frame_size()[0], 0)
        else:
            return (screen_dim[0] // 2, 0)

    
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
        camera_frame = self.video_config.camera.read_frame()

        if camera_frame is None:
            return

        video_frame = self.video_config.video.read_frame()

        if video_frame is None:
            return

        pose_camera = PoseFrame(camera_frame, self.video_config.motion_tracker)
        pose_video = PoseFrame(video_frame, self.video_config.motion_tracker)

        # Display the frame
        screen.blit(pose_video.surface(), pose_video.centered_draw_coords(screen.get_size(), True))
        screen.blit(pose_camera.unannotated_surface(), pose_camera.centered_draw_coords(screen.get_size(), False))