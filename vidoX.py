import cv2
import os
from pytube import YouTube

# Get the YouTube video URL or ID from the user
url = input("Enter the YouTube video URL or ID: ")

# Create a new directory to save the video and images
dir_name = "video_frames"
if not os.path.exists(dir_name):
    os.mkdir(dir_name)

# Download the YouTube video using pytube
yt = YouTube(url)
stream = yt.streams.first()
print(f"Video title: {yt.title}")
print(f"Video duration: {yt.length} seconds")
print(f"Video resolution: {stream.resolution}")
print(f"Video file size: {stream.filesize} bytes")
try:
    stream.download(output_path=dir_name)
    video_path = os.path.abspath(os.path.join(dir_name, stream.default_filename))
    print(f"Video downloaded successfully at {video_path}!")
except Exception as e:
    print(f"Error downloading video: {e}")

# Open the video file and extract frames at 0.5-second intervals
cap = cv2.VideoCapture(video_path)
frame_rate = cap.get(cv2.CAP_PROP_FPS)
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
interval = int(frame_rate * 0.5)
for i in range(0, frame_count, interval):
    cap.set(cv2.CAP_PROP_POS_FRAMES, i)
    ret, frame = cap.read()
    if ret:
        sec = int(i / frame_rate)
        filename = os.path.join(dir_name, f"frame_{sec}.jpg")
        cv2.imwrite(filename, frame)
        print(f"Frame saved at {sec} seconds: {filename}")

cap.release()
