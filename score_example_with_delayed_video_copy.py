import cv2
import pygame
import numpy as np
from collections import deque
import copy
import score

try:
    from skellytracker.trackers.mediapipe_tracker.mediapipe_holistic_tracker import (
        MediapipeHolisticTracker,
    )
except:
    print("To use mediapipe_holistic_tracker, install skellytracker[mediapipe]")

# Initialize the Mediapipe Holistic Tracker with specified configurations
tracker = MediapipeHolisticTracker(
    model_complexity=2,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5,
    static_image_mode=False,
    smooth_landmarks=True,
)



# Initialize Pygame and the display
pygame.init()

font = pygame.font.Font(None, 54)  # None uses the default font, 36 is the size

# Start video capture from a file
video_file_path = 'olly.mp4'  # Replace with your video file path
cap = cv2.VideoCapture(video_file_path)
if not cap.isOpened():
    raise Exception("Could not open video file")

# Get the size of the frame
ret, frame = cap.read()
if not ret:
    raise Exception("Could not read frame")

# Set the dimensions of the window
height, width = frame.shape[:2]
screen = pygame.display.set_mode((2 * width, height))  # Double width for side-by-side display

# Frame and tracking data delay setup
frame_delay = 40  # Delay in frames
tracking_buffer = deque(maxlen=frame_delay)  # Buffer to hold frames and tracking data for delay

# Main loop
running = True
while running:

    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        break  # Break the loop if no frames to read (end of video)

    # Process current frame with tracker
    tracked_objects = tracker.process_image(frame)
    annotated_img = tracker.annotated_image

    # Store the frame and tracking data in the buffer
    deep_copied_tracked_objects = copy.deepcopy(tracked_objects)
    tracking_buffer.append((annotated_img, deep_copied_tracked_objects))

    # Convert the current annotated image for display in Pygame
    frame_current = np.rot90(annotated_img)
    frame_current = cv2.cvtColor(frame_current, cv2.COLOR_BGR2RGB)
    frame_surface_current = pygame.surfarray.make_surface(frame_current)

    # Check if we have enough frames for the delay
    if len(tracking_buffer) == frame_delay:
        frame_delayed, tracked_objects_delayed = tracking_buffer[0]  # Get the delayed frame and tracked data
        frame_delayed = np.rot90(frame_delayed)
        frame_delayed = cv2.cvtColor(frame_delayed, cv2.COLOR_BGR2RGB)
        frame_surface_delayed = pygame.surfarray.make_surface(frame_delayed)

        landmarks = tracked_objects["pose_landmarks"].extra["landmarks"]
        landmarks_d = tracked_objects_delayed["pose_landmarks"].extra["landmarks"]


        text = "score: " + str(score.compare_pos_by_landmarks_cosine_similarity(landmarks, landmarks_d))
        text_surface = font.render(text, True, (255, 255, 255))

        # Display both frames side-by-side
        screen.blit(frame_surface_current, (0, 0))
        screen.blit(frame_surface_delayed, (width, 0))

        screen.blit(text_surface, (50, 50))


        pygame.display.flip()

    # Check for QUIT event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

# When everything is done, release the capture and close Pygame
cap.release()
pygame.quit()

