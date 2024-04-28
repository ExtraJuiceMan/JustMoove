import cv2
import time
import pygame
import numpy as np
from pygame.font import Font
from skellytracker.trackers.base_tracker.base_tracker import BaseTracker
from scenes.scene import SceneBase
from scenes.title_scene import TitleScene
from video_impl import CV2VideoFrames, VideoFramesBase
from game_state import GameVideoConfiguration, GameState

SCENES = [TitleScene()]

try:
    from skellytracker.trackers.mediapipe_tracker.mediapipe_holistic_tracker import (
        MediapipeHolisticTracker,
    )
except:
    print("To use mediapipe_holistic_tracker, install skellytracker[mediapipe]")
    exit()

def init_game():
    pygame.init()
    
    video_config = GameVideoConfiguration(12, CV2VideoFrames(cv2.VideoCapture(0)), 
        MediapipeHolisticTracker(
        model_complexity=2,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
        static_image_mode=False,
        smooth_landmarks=True,
    ))

    state = GameState(pygame.font.Font(None, 128), pygame.display.set_mode((1920, 1080)))

    if not video_config.video.is_open():
        raise Exception("Could not open video device")

    return video_config, state

def game_loop(video_config: GameVideoConfiguration, state: GameState):
    scene: SceneBase = SCENES[0]

    running = True

    while running:
        start_time = time.time()  # Record the start time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            scene.handle_event(event)


        scene.update()

        scene.render(pygame.display.get_surface())

        pygame.display.flip()

        # Wait until it's time for the next frame
        elapsed = time.time() - start_time
        delay = max(1, int((video_config.frame_interval() - elapsed) * 1000))  # Calculate remaining time in ms
        pygame.time.wait(delay)

    # When everything done, release the capture and close Pygame
    cap.release()
    pygame.quit()


