import os
import pickle
import shutil

MEDIA_DIRECTORY = "library"

class PosePosition:
    def __init__(self, x: float, y: float, z: float, vis: float):
        self.x = x
        self.y = y
        self.z = z
        self.vis = vis

class VideoMetadata:
    def __init__(self, id: int, positions: list[PosePosition]):
        self.id = id
        self.positions = positions

class MediaLibrary:
    def __init__(self):
        self.videos: list[VideoMetadata] = []
        self.next_id = 0

    def load_videos(self):
        with os.scandir(MEDIA_DIRECTORY) as it:
            for entry in it:
                if entry.is_dir() and entry.name.isdigit():
                    id = int(entry.name)

                    if id >= self.next_id:
                        self.next_id = id + 1

                    with open(os.path.join(entry.name, f"{id}.json"), "wb") as f:
                        self.videos.append(pickle.load(f))

    def add_video(self, path: str):
        video_id = str(self.next_id)
        video_dir = os.path.join(MEDIA_DIRECTORY, video_id)

        os.makedirs(video_dir)
        
        shutil.copy(path, os.path.join(MEDIA_DIRECTORY, video_id))

        





