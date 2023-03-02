import os
import re
import cv2
import datetime
from pytube import YouTube

# Get the YouTube video URL or ID from the user
url = input("Enter the YouTube video URL or ID: ")

# Get the transcript from the user
transcript_file = input("Enter the path to the transcript file: ")
with open(transcript_file, "r") as f:
    transcript = f.read()

# Remove timestamps and speaker labels from the transcript
transcript = re.sub(r"\[\d+:\d+\]", "", transcript)
transcript = re.sub(r"\w+:\s?", "", transcript)

# Split the transcript into sentences
sentences = transcript.split("\n")
num_sentences = len(sentences)

# Create a new directory with the current date to save the video and images
today = datetime.date.today()
dir_name = today.strftime("video_frames_%Y-%m-%d")
if not os.path.exists(dir_name):
    os.mkdir(dir_name)

# Download the YouTube video using pytube
yt = YouTube(url)
stream = yt.streams.filter(file_extension='mp4').first()
if stream is not None:
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
        exit()
else:
    print("No suitable stream found for the requested resolution.")
    exit()

# Open the video file and extract frames at intervals based on the number of sentences
cap = cv2.VideoCapture(video_path)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
frame_rate = cap.get(cv2.CAP_PROP_FPS)
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
interval = int(yt.length / num_sentences)
with open(os.path.join(dir_name, "index.html"), "w") as f:
    f.write("<html>\n<body>\n")
    for i in range(0, frame_count, int(frame_rate * interval)):
        cap.set(cv2.CAP_PROP_POS_FRAMES, i)
        ret, frame = cap.read()
        if ret:
            sec = int(i / frame_rate)
            filename = os.path.join(dir_name, f"frame_{sec}.jpg")
            cv2.imwrite(filename, frame)
            print(f"Frame saved at {sec} seconds: {filename}")
            caption = sentences[sec * num_sentences // yt.length]
            f.write(f"<div style='display:inline-block; padding:10px;'>\n")
            f.write(f"<img src='{filename}' width='320' height='180'><br>\n")
            f.write(f"<p style='font-size:12px;'>{caption}</p>\n")
            f.write("</div>\n")
    f.write("</body>\n</html>")
    print("HTML file created successfully!")
    cap.release()
