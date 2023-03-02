from youtube_transcript_api import YouTubeTranscriptApi

# Get the transcript of a YouTube video by its ID or URL
video_id = input("Enter YouTube video ID or URL: ")
transcript = YouTubeTranscriptApi.get_transcript(video_id)

# Print the text of each caption
for caption in transcript:
    print(caption['text'])