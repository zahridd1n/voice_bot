# text_to_speech.py
import requests
import config
def text_to_speech(text: str, user_id: int, message_id: int) -> str:
    file_name = f"response_{user_id}_{message_id}.mp3"

    url = config.TTS_API_URL
    token = config.TTS_API_TOKEN
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
    token = config.TTS_API_TOKEN

    payload = {
        "token": token
    }
    files = [
        ('audio', (audio_path, open(audio_path, 'rb'), 'audio/wav'))
    ]

    response = requests.post(url, data=payload, files=files)

    if response.status_code == 200:
        return response.json().get("text", "Matn topilmadi.")
    else:
        raise Exception(f"Xatolik: {response.status_code}, {response.text}")
