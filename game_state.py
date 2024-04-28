from pygame.font import Font
from skellytracker.trackers.base_tracker.base_tracker import BaseTracker
from media_library import MediaLibrary
from video_impl import RecordedCV2VideoFrames, VideoFramesBase
import pygame

class GameVideoConfiguration:
    def __init__(self, fps: int, video: RecordedCV2VideoFrames, camera: VideoFramesBase, motion_tracker: BaseTracker):
        self.fps = fps
        self.camera = camera
        self.video = video
        self.motion_tracker = motion_tracker

    def frame_interval(self):
        return 1 / self.fps

class GameState:
    def __init__(self, font: Font, screen: pygame.Surface, videos: MediaLibrary):
        self.screen = screen
        self.font = font
        self.videos = videos