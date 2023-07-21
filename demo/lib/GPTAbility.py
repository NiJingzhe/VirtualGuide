import openai
import tiktoken


class GPTAbility(object):

    def __init__(self, api_key, personality = "") -> None:
        openai.api_key = api_key
        openai.organization = "org-CnuVGDChBhQiYfR3jhkgKGMY"
        self.encoder = tiktoken.get_encoding("cl100k_base")
        self.cost = 0
        self.chat_history = [
            {
                "role": "system", 
                "content": '''
You are a guide in Xihu Lake, Hangzhou. You are a typical Jiangnan girl.
Your task is to answer users' question base on the information provided.  
Provide your answer in pure text, remember in Chinese.              
                '''.strip()
            }
        ]

    def user_question_filter(self, user_q):
        '''
        过滤用户输入的问题, 使用gpt-3.5-turbo模型
        '''
        message = [
            {"role": "system", "content": '''
Your task is to correct any syntactical errors in user's question, 
and replace or modify any colloquial expressions to make them more formal.
                                          '''.strip()
             
            },
            {"role": "user", "content": user_q}
        ]
        return openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=message,
            temperature=0.0
        )["choices"][0]["message"]["content"].strip()

    def user_question_classification(self, user_q, tag_list):
        '''
        使用GPT模型的few shot能力实现问题的分类
        '''
        task = '''
You will be presented with users' question and your job is to provide a set of tags from the following list.
Provide your answer in json form like {"tags":["tag1", "tag2",...]}. 
Choose ONLY from the list of tags provided here:
'''
        for tag in tag_list:
            task += "- "+ tag + "\n"
        task.strip('\n')

        return str(openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": task},
                {"role": "user", "content": user_q}
            ],
            temperature=0.0,
        )["choices"][0]["message"]["content"]).strip()

    def combine_answer(self, question, answer_list=[], stream=False):
        '''
        把答案列表转换成一个答案, 用GPT-3.5-turbo模型
        '''
        answer = ""
        for ans in answer_list:
            answer += ans+'\n'

        message = {
                "role": "user",
                "content": "information: " + answer+"\nquestion: "+question
        }

        self.chat_history.append(message)

        final_answer: str = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.chat_history,
            stop=None,
            stream=stream
        )

        gpt_answer = []
        gpt_answer_str = ""
        if stream:
            for chunk in final_answer:
                gpt_answer.append(chunk["choices"][0]["delta"])
                
            gpt_answer_str = "".join([m.get('content','') for m in gpt_answer])
            self.chat_history.append({"role": "assistant", "content": gpt_answer_str})

        if not stream:
            final_answer = final_answer["choices"][0]["message"]["content"]
            return final_answer.strip()
        else:
            return final_answer
        
    def chat(self, user_q, stream=False):
        '''
        使用GPT-3.5-turbo模型实现对话
        '''
        message = {
                "role": "user",
                "content": user_q
        }

        self.chat_history.append(message)

        final_answer: str = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.chat_history,
            stop=None,
            stream=stream
        )

        gpt_answer = []
        gpt_answer_str = ""
        if stream:
            for chunk in final_answer:
                gpt_answer.append(chunk["choices"][0]["delta"])
                
            gpt_answer_str = "".join([m.get('content','') for m in gpt_answer])
            self.chat_history.append({"role": "assistant", "content": gpt_answer_str})

        if not stream:
            final_answer = final_answer["choices"][0]["message"]["content"]
            return final_answer.strip()
        else:
            return final_answer
        
    def sound2text(self, sound_file):
        '''
        使用Wishper模型实现语音转文字
        '''
        audio_file= open(sound_file, "rb")
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
        audio_file.close()
        return transcript["text"]