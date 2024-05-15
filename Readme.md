# Env

- Python3.10

* ASR: Whisper(Local)
* MT: Glosbe(Online)
* TTS: TTS: coqui(Local)
* MIX: moviepy, pydub, spleeter

## main.py -> entry

### Create a virtual env and active it
python3 -m venv

### Install the requirements
pip install -r requirements.txt

### Lunch the application
uvicorn main:app_fastapi --port 8001 --reload

## ___<(^-^)>__ Enjoy it

