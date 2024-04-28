import yt_dlp as yt
import os
import ffmpeg
from yt_dlp.utils import download_range_func


def download_video(video_url):
    ydl_opts = {'outtmpl': 'library/%(title)s.%(ext)s'}
    with yt.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])
    # Simple download based on the URL


def download_shortened_video(video_url, start_time, end_time):
    # Takes parameters for how long the video should run
    yt_opts = {
        'verbose': True,
        'download_ranges': yt.utils.download_range_func(None, [(start_time, end_time)]),
        'force_keyframes_at_cuts': True,
        'outtmpl': 'library/%(title)s.%(ext)s'
    }

    with yt.YoutubeDL(yt_opts) as ydl:
        ydl.download([video_url])


if __name__ == "__main__":
    # Replace with your desired video URL, start time, and end time
    youtube_video_url = "https://www.youtube.com/watch?v=60ItHLz5WEA"
    start_time = 2  # Accepts decimal value like 2.3
    end_time = 7

    # Create the "library" folder if it doesn't exist
    os.makedirs("library", exist_ok=True)

    download_shortened_video(youtube_video_url, start_time, end_time)


