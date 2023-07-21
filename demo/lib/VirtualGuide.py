from lib.API_KEY import API_KEY
from lib.QASNet import QASNet
from lib.GPTAbility import GPTAbility
import json
import time

class VirtualGuide(object):

    def __init__(self, model_path, question_lib_path) -> None:
        self.qas_net = QASNet(model_path, question_lib_path)
        self.gpt_ability = GPTAbility(API_KEY)
        
    def answer(self, user_q):
        user_q_filtered = self.gpt_ability.user_question_filter(user_q)
        tag_list = ["casual conversation", "scenic spot information", "question need map to answer"]
        #print(self.gpt_ability.user_question_classification(user_q_filtered, tag_list))
        user_q_tags = json.loads(self.gpt_ability.user_question_classification(user_q_filtered, tag_list))["tags"]
        
        print("question: "+user_q_filtered, "   Its tags: "+str(user_q_tags))

        final_answer = None
        if "scenic spot information" in user_q_tags:
            q_v_a_list = self.qas_net.ann_search(user_q_filtered, 3)
            need_add = False
            answer_list = []
            if q_v_a_list == []:
                need_add = True
                print("No similar question found, searching on internet...")
                answer = self.qas_net.search_on_internet(user_q_filtered)
                answer_list.append(answer)
            else:
                for q_v_a in q_v_a_list:
                    answer_list.append(q_v_a[2])

            final_answer = self.gpt_ability.combine_answer(user_q_filtered, answer_list)

            if need_add:
                self.qas_net.add_question(user_q_filtered, final_answer)
                need_add = False
        elif "casual conversation" in user_q_tags:
            final_answer = self.gpt_ability.chat(user_q_filtered)

        elif "question need map to answer" in user_q_tags:
            print("功能尚未实现")

        print("Virtual Guide: ")
        print(final_answer)

    def hear_question(self, sound_file):

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
            #print("current rms is: " + str(rms))

            # 检测音量
            if not recording and rms > threshold_start:
                recording = True
                #print("Recording started")

            # 开始录音
            if recording:
                frames.append(data)

            # 停止录音
            if recording and rms < threshold_stop:
                recording = False
                #print("Recording stopped")

                # 关闭音频流和PyAudio对象
                stream.stop_stream()
                stream.close()
                p.terminate()

                # 保存录制的音频
                wf = wave.open(sound_file, "wb")
                wf.setnchannels(channels)
                wf.setsampwidth(p.get_sample_size(sample_format))
                wf.setframerate(fs)
                wf.writeframes(b"".join(frames))
                wf.close()

                break

        return self.gpt_ability.sound2text(sound_file)