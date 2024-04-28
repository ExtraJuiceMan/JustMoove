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
    ydl_opts = {
        'verbose': True,
        'format': '[ext=mp4]',
        'download_ranges': download_range_func(None, [(start_time, end_time)]),
        'force_keyframes_at_cuts': True,
        'outtmpl': 'library/%(title)s.%(ext)s'
        }

    with yt.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])


if __name__ == "__main__":
    # Replace with your desired video URL, start time (in seconds), and end time (in seconds)
    youtube_video_url = "https://youtu.be/PCN3ZQ9CHR4?feature=shared"
    start_time = 5
    end_time = 18

    # Create the "library" folder if it doesn't exist
    os.makedirs("library", exist_ok=True)

    download_shortened_video(youtube_video_url, start_time, end_time)




