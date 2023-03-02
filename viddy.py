import os
import time
import subprocess
import cv2
import pytesseract
from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi

# Download the YouTube video
url = input("Enter YouTube video URL: ")
yt = YouTube(url)
video = yt.streams.filter(adaptive=True, file_extension='mp4').first()
video_path = video.download()

# Extract the transcript of the video
transcript = YouTubeTranscriptApi.get_transcript(yt.video_id)

# Create a folder to store the captured images
if not os.path.exists('images'):
    os.makedirs('images')

# Capture images every 5 seconds and extract transcribed text
cap = cv2.VideoCapture(video_path)
frame_rate = cap.get(cv2.CAP_PROP_FPS)
count = 0
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    if count % (5 * frame_rate) == 0:
        image_path = f"images/frame_{count}.jpg"
        cv2.imwrite(image_path, frame)
        text = pytesseract.image_to_string(frame)
        text_path = f"images/frame_{count}.txt"
        with open(text_path, 'w') as f:
            f.write(text)
    count += 1

# Combine captured images and transcribed text
for i in range(count // (5 * frame_rate)):
    image_path = f"images/frame_{i * 5 * frame_rate}.jpg"
    text_path = f"images/frame_{i * 5 * frame_rate}.txt"
    image = cv2.imread(image_path)
    with open(text_path, 'r') as f:
        text = f.read()
    cv2.putText(image, text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.imwrite(f"images/combined_frame_{i}.jpg", image)
    
# Convert the combined images into a video
subprocess.call(['ffmpeg', '-framerate', str(frame_rate // 5), '-i', 'images/combined_frame_%d.jpg', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', 'output.mp4'])
