from moviepy.editor import VideoFileClip
import speech_recognition as sr
import os

pwd = os.getcwd()

video_path = os.path.join(pwd, 'data_reprocess/a_input.mp4')
print('video_path:', video_path)
audio_path = os.path.join(pwd, 'data_reprocess/a_audio.wav')
print('audio_path:', audio_path)
align_file_path = os.path.join(pwd, 'data_reprocess/a_input.txt')
print('align_file_path:', align_file_path)

def extract_audio_from_video(video_path, audio_path):
    video_clip = VideoFileClip(video_path)
    audio_clip = video_clip.audio
    audio_clip.write_audiofile(audio_path)

def recognize_speech_from_file(file_path):
    recognizer = sr.Recognizer()

    with sr.AudioFile(file_path) as source:
        audio = recognizer.record(source)

    return recognizer.recognize_google(audio)

def format_align_file(transcription):
    # For simplicity, let's assume that the words in the transcription are separated by spaces
    words = transcription.split()

    # Set the total duration of the video (in milliseconds)
    total_duration = 74500

    # Calculate the approximate duration of each word
    word_duration = total_duration / len(words)

    align_file_content = ""

    start_time = 0
    for i, word in enumerate(words):
        end_time = start_time + word_duration
        align_file_content += f"{start_time} {end_time} {word}\n"
        start_time = end_time

    return align_file_content

extract_audio_from_video(video_path, audio_path)
transcription = recognize_speech_from_file(audio_path)
align_file_content = format_align_file(transcription)

with open(align_file_path, "w") as align_file:
    align_file.write(align_file_content)
