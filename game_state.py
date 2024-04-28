from pygame.font import Font
from skellytracker.trackers.base_tracker.base_tracker import BaseTracker
from video_impl import VideoFramesBase
import pygame

class GameVideoConfiguration:
    def __init__(self, fps: int, camera: VideoFramesBase, motion_tracker: BaseTracker):
        self.fps = fps
        self.camera = camera
        self.motion_tracker = motion_tracker

    def frame_interval(self):
        return 1 / self.fps

class GameState:
    def __init__(self, font: Font, screen: pygame.Surface):
        self.screen = screen
        self.font = font