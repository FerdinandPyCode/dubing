from pydub import AudioSegment
from pydub.playback import play
from moviepy.editor import AudioFileClip, concatenate_audioclips
import os
from ASR_MT.script import get_transcript, extract_audio_from_video , download
from VS.script import text_to_speech, mix_video


def app(name, source_language, target_language):
    
    print(source_language, target_language)
    # Normalizing yoruba langage code
    if source_language == 'yor':
        source_language = 'yo'
    if target_language == 'yor':
        target_language = 'yo'
    print(source_language, target_language)
    # """
    # SEED
    # """
    print("SEED")
    VIDEO_SAVE_DIRECTORY = "./out/data/"
    
    if not os.path.exists(VIDEO_SAVE_DIRECTORY):
        # Créer le dossier s'il n'existe pas
        os.makedirs(VIDEO_SAVE_DIRECTORY)
    
    print("START")
    
    """
    PREPROCESSING
    """
    print("PREPROCESSING...")
    # Send original video path
    original_video = download(name, VIDEO_SAVE_DIRECTORY)
    
    files = os.listdir(VIDEO_SAVE_DIRECTORY)
    extract_audio_from_video(VIDEO_SAVE_DIRECTORY + files[-1],f"./{name}.mp3", name)
        
    """
    ASR & MT
    """
    print("ASR & MT")
    # Send original and translated subtitle file path
    subtitles = get_transcript(name, source_language, target_language)

    # """
    # TTS
    # """
    # print("TTS")
    # text_to_speech(name, source_language, target_language)

    # """
    # COLLAPSE
    # """
    # print("start collapse ...")
    # print('COLLAPSE')
    # # Spécifiez le chemin du dossier (up or not)
    # chemin_dossier = "./" + name + "/up/"

    # # Obtenez la liste des fichiers dans le dossier
    # liste_fichiers = os.listdir(chemin_dossier)

    # nbre_file = 0
    
    # # Liste des fichiers audio à coller
    # print("Liste des fichiers audio à coller")
    # for fichier in liste_fichiers:
    #     if "up.mp3" in fichier:
    #         nbre_file += 1

    # audio_files = []
    # for i in range(nbre_file):
    #     audio_files.append(f"./{name}/up/tts{i+1}-up.mp3")

    # # Chargez chaque fichier audio en tant que clip audio
    # audio_clips = [AudioFileClip(file) for file in audio_files]

    # # Concaténez les clips audio pour les fusionner
    # final_audio = concatenate_audioclips(audio_clips)

    # # Exportez le fichier audio final
    # final_audio.write_audiofile(name + "_final.mp3")

    # # Fermez les clips audio
    # for clip in audio_clips:
    #     clip.close()
    # print("end collapse ...")

    # """
    # MIX
    # """
    # # MIX AUDIO
    # print(" MIX AUDIO")
    # # Chargez le premier fichier audio
    # audio1 = AudioSegment.from_file("./sortie/" + name + "/accompaniment.wav", format="wav")

    # # Chargez le deuxième fichier audio 
    # audio2 = AudioSegment.from_file(name + "_final.mp3", format="mp3")

    # # Ajustez le volume du deuxième fichier audio selon vos besoins
    # audio1 = audio1 - 20  # Réduisez le volume de X dB (ajustez selon vos besoins)

    # # Mélangez les deux fichiers audio
    # mixed_audio = audio1.overlay(audio2)

    # # Enregistrez le résultat dans un nouveau fichier
    # mixed_audio.export(name + "_mixed_audio.mp3", format="mp3")

    # # MIX VIDEO
    # if not os.path.exists("./out/result/"):
    #     # Créer le dossier s'il n'existe pas
    #     os.makedirs("./out/result/")

    # # mix video
    # print("mix video")
    # dub_video = mix_video(VIDEO_SAVE_DIRECTORY + files[-1], name + "_mixed_audio.mp3", "./out/result/" + name + "_mixed.mp4")
    
    print("END")

    ori_link = original_video.split('.')[1] if '.' in original_video else original_video

    return {
        "original_video": ori_link,
        "original_sub": subtitles["original"],
        "translated_sub": subtitles["translated"],
        # "dub_video": dub_video
    }