import pyaudio
import wave
import audioop

# 设置音频参数
chunk = 1024  # 每次读取的音频流的大小
sample_format = pyaudio.paInt16  # 音频样本的格式
channels = 1  # 声道数
fs = 44100  # 采样率
threshold_start = 120  # 音量阈值
threshold_stop = 30

# 创建PyAudio对象
p = pyaudio.PyAudio()

# 打开音频流
stream = p.open(format=sample_format,
                channels=channels,
                rate=fs,
                frames_per_buffer=chunk,
                input=True)

# 初始化录音标志和缓冲区
recording = False
frames = []

# 持续监听音频流
while True:
    # 读取音频流
    data = stream.read(chunk)

    # 计算音量
    rms = audioop.rms(data, 2)
    print("current rms is: " + str(rms))

    # 检测音量
    if not recording and rms > threshold_start:
        recording = True
        print("Recording started")

    # 开始录音
    if recording:
        frames.append(data)

    # 停止录音
    if recording and rms < threshold_stop:
        recording = False
        print("Recording stopped")

        # 关闭音频流和PyAudio对象
        stream.stop_stream()
        stream.close()
        p.terminate()

        # 保存录制的音频
        wf = wave.open("output.wav", "wb")
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(sample_format))
        wf.setframerate(fs)
        wf.writeframes(b"".join(frames))
        wf.close()

        break