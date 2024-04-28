from skellytracker.trackers.base_tracker.base_tracker import BaseTracker
from mediapipe_pose_tracker import MediapipePoseTracker

def create_motion_tracker() -> BaseTracker:
    return MediapipePoseTracker(
            model_complexity=2,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
            static_image_mode=False,
            smooth_landmarks=True,
        )