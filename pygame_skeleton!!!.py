import cv2
import time
import pygame
import numpy as np

try:
    from skellytracker.trackers.mediapipe_tracker.mediapipe_holistic_tracker import (
        MediapipeHolisticTracker,
    )
except:
    print("To use mediapipe_holistic_tracker, install skellytracker[mediapipe]")


tracker = MediapipeHolisticTracker(
    model_complexity=2,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5,
    static_image_mode=False,
    smooth_landmarks=True,
)



# Initialize Pygame and the display
pygame.init()
fps = 12  # Desired frame rate
frame_interval = 1 / fps  # Interval between frames in seconds

# Start video capture
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise Exception("Could not open video device")

# Get the size of the frame
ret, frame = cap.read()
if not ret:
    raise Exception("Could not read frame")

# Set the dimensions of the window
height, width = frame.shape[:2]
screen = pygame.display.set_mode((width, height))

# Define font for the text
font = pygame.font.Font(None, 128)  # None for default font, size 36

# Main loop
running = True
while running:
    start_time = time.time()  # Record the start time

    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        break

    tracker.process_image(frame)
    annotated_img = tracker.annotated_image

    # Convert the frame from BGR to RGB
    #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Convert the frame to a surface to display in Pygame
    frame = np.rot90(annotated_img)
    frame_surface = pygame.surfarray.make_surface(frame)

    # Display the frame
    screen.blit(frame_surface, (0, 0))

    # Render text over the frame
    text_surface = font.render('Dance Game!', True, (255, 255, 255))  # White text
    screen.blit(text_surface, (10, 10))  # Position the text at the top-left corner

    pygame.display.flip()

    # Check for QUIT event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Wait until it's time for the next frame
    elapsed = time.time() - start_time
    delay = max(1, int((frame_interval - elapsed) * 1000))  # Calculate remaining time in ms
    pygame.time.wait(delay)

# When everything done, release the capture and close Pygame
cap.release()
pygame.quit()


