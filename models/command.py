from pytube import YouTube

# YouTube video URL
video_url = "https://www.youtube.com/watch?v=1_gqlbADaAw"

# Download location on Desktop
output_path = "/home/user/Desktop"  # Replace 'user' with your actual username

# Create YouTube object
yt = YouTube(video_url)

# Get the highest resolution video stream
video = yt.streams.get_highest_resolution()

# Download the video to the specified path
video.download(output_path)
