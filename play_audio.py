import pyaudio
import base64
import numpy as np


def play_wav_base64(base64_audio):
    # 创建 PyAudio 对象
    p = pyaudio.PyAudio()

    # 解码 Base64 编码的 WAV 字符串为字节数据
    audio_bytes = base64.b64decode(base64_audio)

    # 将字节数据转换为可播放的音频数据（这里使用 NumPy）
    audio_data = np.frombuffer(audio_bytes, dtype=np.int16)

    # 打开音频流
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, output=True)

    # 播放音频数据
    stream.start_stream()
    stream.write(audio_data.tobytes())
    stream.stop_stream()
    stream.close()

    # 关闭 PyAudio 对象
    p.terminate()
