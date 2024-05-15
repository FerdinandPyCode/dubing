from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import WebVTTFormatter
from moviepy.editor import VideoFileClip
from pytube import YouTube
import os
from spleeter.separator import Separator
from VS.mt import translate_text

def download(video_url, VIDEO_SAVE_DIRECTORY):
    """Downlaod youtube video by getting the id

    Args:
        video_url (str): video url
        VIDEO_SAVE_DIRECTORY (str): video directory
        
    Returns:
        str: downloaded video path
    """
    video = YouTube("https://www.youtube.com/watch?v=" + video_url)
    video = video.streams.get_highest_resolution()
    path = ""
    
    try:
        path = video.download(VIDEO_SAVE_DIRECTORY)
    except:
        print("Failed to download video")

    print("video was downloaded successfully")
    
    return path
    
    
def extract_audio_from_video(video_path, audio_output_path, video_id):
    # Load the video clip
    video_clip = VideoFileClip(video_path)
    
    # Extract audio from the video
    audio_clip = video_clip.audio
    
    # Save the audio as a WAV file
    audio_clip.write_audiofile(audio_output_path)

    """
    Voice and noise separator
    """
    separator = Separator('spleeter:2stems')

    input_audio = audio_output_path
    output_path = './sortie/'

    separator.separate_to_file(input_audio, output_path)

def get_transcript(video_id, lgA, lgB):
    """Function to get video transcript

    Args:
        video_id (str): video id
        lgA (str): source language
        lgB (str): target language

    Returns:
        dic: dictionnary of original and translated subtitle
    """
    print(video_id,lgA,lgB)
    transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[lgA])
    
    subtitles = {
        "original": "",
        "translated": ""
    }
    # print(transcript)
    subtitles["original"] = formater(video_id, transcript, lgA)

    # print(subtitles["original"])
      
    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

    # print(transcript_list)
    print(transcript)
    transcript = transcript_list.find_transcript([lgA])
    if lgB == 'fon':
        index = 0
        new_trans = transcript
        for step in new_trans:
            print(f'step trans fon {index} / {len(new_trans)}')
            fon_trans = translate_text(step['text'])
            transcript[index]['text'] = fon_trans
            index += 1

        print(new_trans)
        print(transcript)
        
    else:
        transcript = transcript.translate(lgB).fetch()
    
    subtitles["translated"] = formater(video_id, transcript, lgB, False)
    print(subtitles["translated"])
    return subtitles


def formater(video_id, transcript, lg, original=True):
    """format transcript to vtt

    Args:
        video_id (str): the youtube video id
        transcript (json): _description_
        lg (str): language like 'fr', 'en'
        original (bool): condition variable. Defaults to True.

    Returns:
        str: subtitle vtt file path
    """
    
    formatter = WebVTTFormatter()
    
    # .format_transcript(transcript) turns the transcript into a VTT string.
    vtt_formatted = formatter.format_transcript(transcript)
    
    if not original:
        file_name = video_id + "-" + lg + '.vtt'
    else: 
        file_name = video_id + '.vtt'

    # Now we can write it out to a file.
    with open(file_name, 'w', encoding='utf-8') as vtt_file:
        vtt_file.write(vtt_formatted)
        
    return file_name