from fastapi import FastAPI, HTTPException
from typing import Optional

from fastapi.staticfiles import StaticFiles
from ASR_MT.script import get_transcript
from script import app
from fastapi.middleware.cors import CORSMiddleware

from script_completed import app_dubbing

app_fastapi = FastAPI()
origins = ["*"]

app_fastapi.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app_fastapi.post("/translate/subtitle/")
async def translate_video(
    name: str,
    source_language: str,
    target_language: str
):
    try:
        result = app(name, source_language, target_language)
        result["original_video"]=result["original_video"].replace('/out/',"")+'.mp4'
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app_fastapi.post("/translate/dubbing-agbalagba/")
async def translate_video(
    name: str,
    source_language: str,
    target_language: str
    ):

    try:
        result = app_dubbing(name, source_language, target_language)
        result["original_video"]=result["original_video"].replace('/out/',"")+'.mp4'
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


app_fastapi.mount("/video", StaticFiles(directory="./out"), name="output")
app_fastapi.mount("/vtt", StaticFiles(directory='.'), name="root")