from moviepy.editor import *
import os
from pydub import AudioSegment
from moviepy.editor import VideoFileClip, AudioFileClip, clips_array
from gtts import gTTS
import torch
import requests
from TTS.api import TTS
from VS.ftts_fon_yor import *
from transformers import pipeline

def inference(text, file_path):

    CHUNK_SIZE = 1024
    url = "https://api.elevenlabs.io/v1/text-to-speech/ErXwobaYiN019PkySvjV"

    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": "ed5ae2b7946c6edc20be3226aca7c6c2"
    }

    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5
        }
    }

    response = requests.post(url, json=data, headers=headers)
    with open(file_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
            if chunk:
                f.write(chunk)

def formatter(lg):
    if lg == "en":
        return "eng"
    if lg == "fr":
        return "fra"
    # ADD LANGUAGE
    
def mix_video(old_video, new_audio, new_video):
    """to mix video

    Args:
        old_video (str): old video without sound path
        new_audio (str): new audio path
        new_video (str): new video (mixed)

    Returns:
        str: the new video path
    """
    
    video_clip = VideoFileClip(old_video)  
    audio_clip = AudioFileClip(new_audio)  

    video_clip = video_clip.set_audio(audio_clip)

    video_clip.write_videofile(new_video, codec="libx264")

    # TODO: Ajustement de mixage
    
    return new_video

def augmenter_silence(input_audio, output_audio, duree_augmentation_sec):
    # Charger le fichier audio existant
    audio_existant = AudioSegment.from_file(input_audio)

    # Générer une piste audio de silence avec la durée spécifiée
    silence_audio = AudioSegment.silent(duration=duree_augmentation_sec * 1000)  # en millisecondes

    # Concaténer le silence avec le fichier audio existant
    audio_augmente = silence_audio + audio_existant + silence_audio
    
    # Sauvegarder le fichier audio augmenté
    audio_augmente.export(output_audio, format="mp3")

def text_to_speech(project_name, lgA, lgB):
    os.makedirs(project_name, exist_ok=True)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    
    with open(f'{project_name}-{lgB}.vtt', "r") as fichier:
        tab = fichier.readlines()
        i = 1
        time = 0.0
        
        print("start speech ...")
        
        tts = None
        pipe = None
        if(lgB == 'yo'):
            # TTS YOR
            device = "cuda" if torch.cuda.is_available() else "cpu"
            tts = TTS("tts_models/yor/openbible/vits").to(device)
            print("LOading tts_models OKAY")
        elif (lgB == 'fon'):
            pipe = pipeline("text-to-speech", model="facebook/mms-tts-fon")
            print("Loading facebook/mms-tts-fon OKAY")
        
        # 
        for el in tab[2:]:
            
            print("---------->", i)
            # Get time for next processing
            if '-->' in el:
                start, end = el.split("-->")
                
                # start_min, start_sec= [float(i) for i in start.split(":")]
                # end_min, end_sec= [float(i) for i in end.split(":")]
                
                _, start_min, start_sec= [float(i) for i in start.split(":")]
                _, end_min, end_sec= [float(i) for i in end.split(":")]

                time = ((end_min*60)+end_sec) - ((start_min*60)+start_sec)

            # Get voice synthetis
            if el != '\n' and '-->' not in el:
                # Eleven labs inference
                # inference(el[:-1], file_path=str("./"+project_name+"/tts"+str(i)+".wav"))
                if(lgB == 'yo'):
                    # TTS YOR
                    text_to_speech_yor(tts,el[:-1],str("./"+project_name+"/tts"+str(i)+".wav"))

                elif (lgB == 'fon'):
                    text_to_speech_fon(pipe,el[:-1],str("./"+project_name+"/tts"+str(i)+".wav"))
                else:
                    print("<---gTTS---->")
                    tts = gTTS(text=el[:-1], lang= lgB, slow=False)
                    tts.save(str("./"+project_name+"/tts"+str(i)+".wav"))
            
                print("Audio saved")

                """
                    AUDIO FITTING
                """
                path = "./"+project_name+"/"

                # Charger le fichier audio
                audio = AudioSegment.from_file(path+"tts"+str(i)+".wav")

                duration = len(audio) / 1000

                # Calculer le ratio de rapidité
                coef = duration / time
                
                new_audio =  f"./{project_name}/up/tts{i}-up.mp3"

                if not os.path.exists(f"./{project_name}/up/"):
                    # Créer le dossier s'il n'existe pas
                    os.makedirs(f"./{project_name}/up/")

                ##

                if coef < 1.001:
                    part_time_silence =  (time - duration) / 2
                    augmenter_silence(path+"tts"+str(i)+".wav", new_audio, part_time_silence)  # 60 secondes d'augmentation
                else:
                    # Augmenter la vitesse (coef=1.5 signifie coef=1.5 fois plus rapide)
                    audio_augmente = audio.speedup(playback_speed=coef)

                    # Sauvegarder le fichier audio augmenté de vitesse
                    audio_augmente.export(new_audio, format='mp3')

                    # Fermer le fichier audio d'origine
                    # audio.close()

                i += 1
                print(i)
                
        print("end speech ...")
    
    
def personalization(project_name, lgA, lgB, data):
    os.makedirs(project_name, exist_ok=True)
    
    lg = "yor"
    
    device = "cuda" if torch.cuda.is_available() else "cpu"

    with open(f'{project_name}-{lgB}.vtt', "r") as fichier:
        tab = fichier.readlines()
        i = 1
        time = 0.0
        
        print("start speech ...")
        step = 0
        
        for el in tab[2:]:

            # Get time for next processing
            if '-->' in el:
                start, end = el.split("-->")
                
                _, start_min, start_sec= [float(i) for i in start.split(":")]
                _, end_min, end_sec= [float(i) for i in end.split(":")]

                time = ((end_min*60)+end_sec) - ((start_min*60)+start_sec)

            text = el[:-1]
            
            for elm in data:
                if elm[-1] == step:
                    text = elm[1]
                
            # Get voice synthetis
            if el != '\n' and '-->' not in el:
                inference(text, file_path=str("./"+project_name+"/tts"+str(i)+".wav"))

                """
                    AUDIO FITTING
                """
                path = "./"+project_name+"/"

                # Charger le fichier audio
                audio = AudioSegment.from_file(path+"tts"+str(i)+".wav")

                duration = len(audio) / 1000

                # Calculer le ratio de rapidité
                coef = duration / time
                
                new_audio = f"./{project_name}/up/tts{i}-up.mp3"

                if coef < 1.001:
                    part_time_silence =  (time - duration) / 2
                    augmenter_silence(path+"tts"+str(i)+".wav", new_audio, part_time_silence)  # 60 secondes d'augmentation
                else:
                    # Augmenter la vitesse (coef=1.5 signifie coef=1.5 fois plus rapide)
                    audio_augmente = audio.speedup(playback_speed=coef)

                    # Sauvegarder le fichier audio augmenté de vitesse
                    audio_augmente.export(new_audio, format='mp3')

                    # Fermer le fichier audio d'origine
                    # audio.close()

                i += 1
                print(i)
                
            step += 1
                
             
        print("end speech ...")
   