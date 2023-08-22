import pyaudio
import wave
import webrtcvad
import base64
import io


class AudioRecorder:
    def __init__(self):
        # 创建VAD对象
        self.vad = webrtcvad.Vad()

        # 设置VAD的模式，0-3，0最不敏感，3最敏感
        self.vad.set_mode(3)

        # 配置录音参数
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 16000
        self.CHUNK = 480  # 30ms
        self.MAX_DELAY_COUNT = 50

        # 创建PyAudio对象
        self.audio = pyaudio.PyAudio()

        # 打开音频流
        self.stream = self.audio.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            frames_per_buffer=self.CHUNK,
        )

        # 初始化录音状态
        self.recording = False
        self.delay_count = 0
        self.frames = []

    def start_recording(self):
        # print("开始录音...")
        while True:
            # 读取音频数据
            data = self.stream.read(self.CHUNK, exception_on_overflow=False)
            is_speech = self.vad.is_speech(data, self.RATE)

            if is_speech:
                self.delay_count = 0

            # 检测是否有语音
            if is_speech and not self.recording:
                # print("检测到语音开始")
                self.frames = []
                self.recording = True

            if self.recording:
                self.frames.append(data)

            if not is_speech:
                self.delay_count += 1

            if self.recording and self.delay_count > self.MAX_DELAY_COUNT:
                # print("检测到语音结束")
                self.recording = False

                if len(self.frames) > 0:
                    # 保存音频数据为WAV文件
                    audio_buffer = io.BytesIO()
                    wave_file = wave.open(audio_buffer, "wb")
                    wave_file.setnchannels(self.CHANNELS)
                    wave_file.setsampwidth(self.audio.get_sample_size(self.FORMAT))
                    wave_file.setframerate(self.RATE)
                    wave_file.writeframes(b"".join(self.frames))
                    wave_file.close()
                    audio_data = audio_buffer.getvalue()
                    return base64.b64encode(audio_data).decode()

    def close(self):
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()
