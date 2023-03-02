import cv2
import os
from pytube import YouTube

# Get the YouTube video URL or ID from the user
url = input("Enter the YouTube video URL or ID: ")

# Download the YouTube video using pytube
yt = YouTube(url)
stream = yt.streams.first()
print(f"Video title: {yt.title}")
print(f"Video duration: {yt.length} seconds")
print(f"Video resolution: {stream.resolution}")
print(f"Video file size: {stream.filesize} bytes")
try:
    stream.download()
    video_path = os.path.abspath(stream.default_filename)
    print(f"Video downloaded successfully at {video_path}!")
except Exception as e:
    print(f"Error downloading video: {e}")

# Open the video file and extract frames at 1-second intervals
cap = cv2.VideoCapture(video_path)
frame_rate = cap.get(cv2.CAP_PROP_FPS)
count = 0
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    if count % (1 * frame_rate) == 0:
        cv2.imwrite(f"frame_{count}.jpg", frame)
    count += 1

cap.release()
