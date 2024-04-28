import os
import pickle
import shutil
import cv2

from motion_tracker import create_motion_tracker

MEDIA_DIRECTORY = "library"

def get_video_dir_path(id: int):
    return os.path.join(MEDIA_DIRECTORY, str(id))

def get_video_file_path(id: int):
    return os.path.join(get_video_dir_path(id), str(id))

class PosePosition:
    def __init__(self, x: float, y: float, z: float, vis: float):
        self.x = x
        self.y = y
        self.z = z
        self.vis = vis

class VideoMetadata:
    def __init__(self, id: int, positions: list[list[PosePosition]]):
        self.id = id
        self.positions = positions

class MediaLibrary:
    def __init__(self):
        self.videos: dict[int, VideoMetadata] = {}
        self.next_id = 0

    def load_videos(self):
        with os.scandir(MEDIA_DIRECTORY) as it:
            for entry in it:
                if entry.is_dir() and entry.name.isdigit():
                    id = int(entry.name)

                    if id >= self.next_id:
                        self.next_id = id + 1

                    with open(os.path.join(MEDIA_DIRECTORY, entry.name, f"{id}.dat"), "rb") as f:
                        self.videos[id] = pickle.load(f)

    def get_video(self, id: int) -> VideoMetadata:
        return self.videos[id]

    def all_videos(self) -> dict[int, VideoMetadata]:
        return self.videos

    def add_video(self, path: str):
        video_id_int = self.next_id
        video_id = str(self.next_id)
        video_dir = os.path.join(MEDIA_DIRECTORY, video_id)

        os.makedirs(video_dir)
        shutil.copy(path, os.path.join(video_dir, video_id))

        tracker = create_motion_tracker()

        vid_cap = cv2.VideoCapture(path)

        total_frames = vid_cap.get(cv2.CAP_PROP_FRAME_COUNT)

        frame_available, frame = vid_cap.read()

        frame_pose_positions: list[list[PosePosition]] = []

        i = 1
        while frame_available:
            print(f"Processing frame {i}/{total_frames} ({i / total_frames * 100}%)")
            points = tracker.process_image(frame)
            if "pose_landmarks" not in points or points["pose_landmarks"].extra["landmarks"] is None:
                frame_pose_positions.append([])
            else:
                frame_pose_positions.append([PosePosition(x.x, x.y, x.z, x.visibility) for x in points["pose_landmarks"].extra["landmarks"].landmark])

            frame_available, frame = vid_cap.read()
            i += 1

        metadata = VideoMetadata(video_id_int, frame_pose_positions)

        with open(os.path.join(MEDIA_DIRECTORY, video_id, f"{video_id}.dat"), "wb") as f:
            pickle.dump(metadata, f)

        self.videos[video_id_int] = metadata

        return video_id

if __name__ == "__main__":
    media_lib = MediaLibrary()
    media_lib.load_videos()

    path = input("Choose video file path: ")
    print(f"Saving video {path} to media library...")

    vid_id = media_lib.add_video(path)

    print(f"Added video ID {vid_id} to library")




