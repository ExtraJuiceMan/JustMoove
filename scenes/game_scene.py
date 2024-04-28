from typing import Optional

from skellytracker.trackers.base_tracker.base_tracker import BaseTracker
from game_gui import image_resize, image_scaled_dim
from scenes.scene import SceneBase
from game_state import GameVideoConfiguration, GameState
import numpy as np
import pygame
import cv2
import score
from media_library import PosePosition

GAME_RESOLUTION = (1600, 900)

class PoseFrame:
    def __init__(self, frame: np.ndarray, motion_tracker: BaseTracker, pose_positions=None, fit_to=None):
        self.frame = frame
        self.frame = cv2.rotate(self.frame, cv2.ROTATE_90_COUNTERCLOCKWISE, self.frame)

        if pose_positions is None:

            points = motion_tracker.process_image(self.frame)
            coord_stuff =points["pose_landmarks"].extra["landmarks"] 
            if coord_stuff:
                self.pose_positions = [PosePosition(x.x, x.y, x.z, x.visibility) for x in coord_stuff.landmark]
            else:
                self.pose_positions = None

        else:
            self.pose_positions = pose_positions

        self.raw_frame: np.ndarray = frame if pose_positions is None else motion_tracker.raw_image

    def frame_size(self, screen_size=None):
        if screen_size is not None:
            return image_scaled_dim(self.frame.shape, width = screen_size[0] // 2, height = screen_size[1])[::-1]

        return self.frame.shape

    def unannotated_surface(self, screen_size=None) -> pygame.Surface:
        return pygame.surfarray.make_surface(image_resize(cv2.cvtColor(self.raw_frame, cv2.COLOR_BGR2RGB), width = screen_size[0] // 2, height = screen_size[1]))

    def surface(self, screen_size=None) -> pygame.Surface:
        return pygame.surfarray.make_surface(image_resize(cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB), width = screen_size[0] // 2, height = screen_size[1]))

    def centered_draw_coords(self, screen_dim: tuple[int, int], left: bool) -> tuple[int, int]:
        if left:
            return (screen_dim[0] // 2 - self.frame_size(screen_dim)[0], 0)
        else:
            return (screen_dim[0] // 2, 0)
    
class GameScene(SceneBase):
    def __init__(self, video_config: GameVideoConfiguration, state: GameState):
        SceneBase.__init__(self)
        self.video_config = video_config
        self.state = state
        self.clock = pygame.time.Clock()

        background_image = pygame.image.load("images/hackdavis_background.png")
        scale_ratio = GAME_RESOLUTION[0] / background_image.get_size()[0]

        self.background_image = pygame.transform.smoothscale(
            background_image,
            (background_image.get_size()[0] * scale_ratio, background_image.get_size()[1] * scale_ratio)
            ).convert()

        self.game_icon = pygame.transform.smoothscale(pygame.image.load("images/menuIcon.png"), (230, 234)).convert_alpha()

    def handle_event(self, event: pygame.event.Event):
        pass
    
    def update(self):
        pass

    def on_load(self):
        self.state.set_resolution(GAME_RESOLUTION)
    
    def render(self, screen: pygame.Surface):
        camera_frame = self.video_config.camera.read_frame()

        if camera_frame is None:
            return

        video_frame = self.video_config.video.read_frame()

        if video_frame is None:
            return

        pose_camera = PoseFrame(camera_frame, self.video_config.motion_tracker)
        pose_video = PoseFrame(video_frame, self.video_config.motion_tracker, self.video_config.video.last_frame_pose())


        c_pos = pose_camera.pose_positions
        v_pos = pose_video.pose_positions

        if c_pos and v_pos:
            sim = score.compare_pos_by_landmarks_cosine_similarity(c_pos, v_pos)
            self.state.score += score.sim_to_positive_score(sim)

        score_text = "score: " + str(self.state.score)
        score_text_surface = self.state.font.render(score_text, True, (255, 255, 255))

        # Display the frame
        screen.blit(self.background_image, (0, 0))
        screen.blit(self.game_icon, (0, screen.get_size()[1] - self.game_icon.get_size()[1]))
        screen.blit(pose_video.surface(screen.get_size()), pose_video.centered_draw_coords(screen.get_size(), True))
        screen.blit(pose_camera.surface(screen.get_size()), pose_camera.centered_draw_coords(screen.get_size(), False))

        self.clock.tick()
        fps = self.state.font.render(f"FPS: {self.clock.get_fps():.2f}", True, (255, 255, 255))
        screen.blit(fps, (8, 0))
        screen.blit(score_text_surface, (50, 50))
