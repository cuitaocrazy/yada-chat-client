import json
import requests
from audio_recorder import AudioRecorder
from play_audio import play_wav_base64

recorder = AudioRecorder()

history = []
while True:
    print("开始录音...")
    wav_base64 = recorder.start_recording()
    print("请求...")
    response = requests.post(
        "http://124.126.140.93:35000/combo",
        data=json.dumps({"wav": wav_base64, "history": history}),
        headers={"Content-Type": "application/json"},
    )
    resp_json = response.json()
    history = resp_json["history"]
    wav_base64 = resp_json["wav"]
    print(history[-1])
    play_wav_base64(wav_base64)
