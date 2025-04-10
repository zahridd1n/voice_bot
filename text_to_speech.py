# text_to_speech.py
import requests
import config
from pydub import AudioSegment
import os


def text_to_speech(text: str, user_id: int, message_id: int) -> str:
    file_name = f"response_{user_id}_{message_id}.mp3"

    url = config.TTS_API_URL
    token = config.API_TOKEN
    speaker_id = config.SPEAKER_ID

    payload = f"token={token}&text={text}&speaker_id={speaker_id}"
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    response = requests.post(url, headers=headers, data=payload)

    if response.status_code == 200:
        with open(file_name, "wb") as f:
            f.write(response.content)
        return file_name
    else:
        raise Exception(f"Error: {response.status_code}, {response.text}")

def speech_to_text(audio_path: str) -> str:
    url = config.STT_API_URL
    token = config.API_TOKEN

    payload = {
        "token": token
    }
    files = [
        ('audio', (audio_path, open(audio_path, 'rb'), 'audio/ogg'))
    ]

    response = requests.post(url, data=payload, files=files)

    if response.status_code == 200:
        return response.json()['message']['result']['text']
    else:
        raise Exception(f"Xatolik: {response.status_code}, {response.text}")





def convert_ogg_to_wav(ogg_path, wav_path):
    try:
        audio = AudioSegment.from_file(ogg_path, format="ogg")
        audio.export(wav_path, format="wav")
        print("Konvertatsiya bajarildi:", wav_path)
        return wav_path
    except Exception as e:
        print("❌ Ovozli xabarda xatolik:", e)
        return None
