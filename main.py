import json
import requests
from audio_recorder import AudioRecorder
from play_audio import play_wav_base64

recorder = AudioRecorder()

history = []
while True:
    wav_base64 = recorder.start_recording()
    print("got a wav")
    response = requests.post(
        "http://localhost:35000/combo",
        data=json.dumps({"wav": wav_base64, "history": history}),
        headers={"Content-Type": "application/json"},
    )
    resp_json = response.json()
    history = resp_json["history"]
    wav_base64 = resp_json["wav"]
    print(history[-1])
    play_wav_base64(wav_base64)
