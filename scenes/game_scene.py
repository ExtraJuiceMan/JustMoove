from typing import Optional
from scenes.scene import SceneBase
from game_state import GameVideoConfiguration, GameState
import numpy as np
import pygame
import cv2

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
        frame_available, video_frame = self.video_config.camera.read_frame()

        if not frame_available:
            return

        video_frame = cv2.rotate(video_frame, cv2.ROTATE_90_COUNTERCLOCKWISE, video_frame)

        pose_positions = self.video_config.motion_tracker.process_image(video_frame)
        unannotated_frame: np.ndarray = self.video_config.motion_tracker.raw_image

        # Convert the frame from BGR to RGB
        #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Convert the frame to a surface to display in Pygame
        frame_surface = pygame.surfarray.make_surface(unannotated_frame)

        # Display the frame
        screen.blit(frame_surface, (0, 0))

        # Render text over the frame
        #text_surface = font.render('Dance Game!', True, (255, 255, 255))  # White text
        #screen.blit(text_surface, (10, 10))  # Position the text at the top-left corner