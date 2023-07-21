from lib.FastSentence2Vec import FastSentence2Vec
import json
from lib.ZhihuSpyder import ZhihuSpyder
import openai
import tiktoken
from lib.API_KEY import API_KEY

class QASNet(object):
    '''
    提供了一个简单的问答系统, 包括一些简单的功能:
    1. ann搜索最邻近问题
    2. 用户问题优化
    3. 用户问题分类
    4. 对于未知问题爬取知乎答案
    5. 多个答案的整合输出
    6. 向问题库中添加问题与答案
    '''

    def __init__(self, model_path, question_lib_path):
        self.sent2vec = FastSentence2Vec()
        self.sent2vec.load(model_path)
        self.question_lib_path = question_lib_path
        self.encoder = tiktoken.get_encoding("cl100k_base")
        

        try:
            with open(self.question_lib_path, mode="r", encoding="utf-8") as input_f:
                self.question_lib = list(json.loads(input_f.read())["data"])
                input_f.close()
        except FileNotFoundError:
            print("No question lib file found, please init the question library first.")
            with open(self.question_lib_path, mode="w", encoding="utf-8") as output_f:
                init_str = json.dumps({"data": [{"Q":"你是谁", "A":"我是这里的导游"}]})
                output_f.write(init_str)
            exit(1)

    def ann_search(self, user_q, top_n, threshold=0.78):
        '''
        返回相似度排名前top_n的问题以及答案
        返回格式为
        [(question1, similarity1, answer1), (question2, similarity2, answer2), ... (questionn, similarityn, answern)]
        '''
        user_q_vec = self.sent2vec.Sent2Vec(user_q)
        similarity = []
        for qa_pair in self.question_lib:
            cos_sim = self.sent2vec.cosine_similarity(
                        user_q_vec, 
                        self.sent2vec.Sent2Vec(qa_pair['Q'])
                    )
            if cos_sim >= threshold:
                similarity.append(
                    (
                        qa_pair['Q'], 
                        cos_sim,
                        qa_pair['A']
                    )
                )
        similarity.sort(key=lambda x: x[1], reverse=True)
        return similarity[:top_n]

    def add_question(self, question : str, answer : str):
        '''
        向问题库中添加问题
        '''
        self.question_lib.append(
            {
                "Q": question,
                "A": answer.strip()
            }
        )

        with open(self.question_lib_path, mode="w", encoding="utf-8") as output_f:
            output_f.write(json.dumps({"data": self.question_lib}))
            output_f.close()

    def search_on_internet(self, question):
        '''
        在知乎上爬取问题答案
        '''
        spyder = ZhihuSpyder()
        answer_list = spyder.grab_topic_to_list(question)
        return answer_list[:2]