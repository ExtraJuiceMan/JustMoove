import yt_dlp as yt


def download_video(video_url, destination_folder):
    ydl_opts = {'outtmpl': f'{destination_folder}/%(title)s.%(ext)s'}
    with yt.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])


if __name__ == "__main__":
    # Replace with your desired video URL and destination folder
    youtube_video_url = "https://www.youtube.com/watch?v=60ItHLz5WEA"
    output_folder = "./youtube_videos/"

    download_video(youtube_video_url, output_folder)
