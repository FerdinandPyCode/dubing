import torch
import torchaudio
from TTS.api import TTS
from transformers import pipeline
import numpy as np
import scipy


def save_audio(audio_data, sample_rate, file_path='output.mp3'):
    """
    Saves an audio array to a WAV file.

    Args:
        audio_data (numpy.ndarray): The audio data as a numpy array.
        sample_rate (int): The sample rate of the audio (in Hz).
        file_path (str): The path where the audio file will be saved.

    Returns:
        None: Outputs an audio file at the specified path.
    """
    # Convert the numpy array to a PyTorch tensor
    tensor = torch.from_numpy(audio_data)

    # Save the tensor as an audio file using torchaudio
    torchaudio.save(file_path, tensor, sample_rate)


def text_to_speech_fon(model,text,output_file="fon.wav"):
    """
    Converts text to speech using a pre-trained model from Hugging Face Transformers.

    Args:
        text (str): The text to be converted to speech.

    Returns:
        None: Outputs a .wav file with the generated speech.
    """
    # Initialize the pipeline with the text-to-speech model
    # Use the pipeline to generate speech from the input text
    output = model(text)

    # Save the audio data to a .wav file
    save_audio(output['audio'], output['sampling_rate'],file_path=output_file)

    return output_file


def text_to_speech_yor(model,text,output_file="yor.mp3"):
    # Get device (GPU or CPU)

    # Init TTS

    # Convert text to speech and save to a file
    model.tts_to_file(text=text, file_path=output_file)
    return output_file



# TTS FON
#pipe = pipeline("text-to-speech", model="facebook/mms-tts-fon")
#text_to_speech_fon(pipe,"Ayixamasɔgbenánɔ, adingbannɔ wɛ nú we")

## TTS YOR
#device = "cuda" if torch.cuda.is_available() else "cpu"
#tts = TTS("tts_models/yor/openbible/vits").to(device)
#text_to_speech_yor(tts,"Omo ilu Benin ni mi ti o duro loni, Olorun daa")