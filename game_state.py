from pygame.font import Font
from skellytracker.trackers.base_tracker.base_tracker import BaseTracker
from media_library import MediaLibrary, VideoMetadata
from video_impl import RecordedCV2VideoFrames, VideoFramesBase
import pygame

class GameVideoConfiguration:
    def __init__(self, fps: int, video_meta: VideoMetadata, video: RecordedCV2VideoFrames, camera: VideoFramesBase, motion_tracker: BaseTracker):
        self.fps = fps
        self.video_meta = video_meta
        self.camera = camera
        self.video = video
        self.motion_tracker = motion_tracker

    def frame_interval(self):
        return 1 / self.fps

    def set_video(self, video: VideoMetadata):
        self.video_meta = video
        self.video = RecordedCV2VideoFrames(video)

class GameState:
    def __init__(self, font: Font, screen: pygame.Surface, videos: MediaLibrary, score: float = 0):
        self.screen = screen
        self.font = font
        self.videos = videos
        self.score = score
        self.download_url = None

    def set_resolution(self, resolution):
        if self.screen.get_size() != resolution:
            self.screen = pygame.display.set_mode(resolution)

    def set_download_url(self, url):
        self.download_url = url