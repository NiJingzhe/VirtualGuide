from lib.FastSentence2Vec import FastSentence2Vec
import json

class QASNet(object):

    def __init__(self, model_path, question_lib_path):
        self.sent2vec = FastSentence2Vec()
        self.sent2vec.load(model_path)
        self.question_lib_path = question_lib_path

        try:
            with open(self.question_lib_path, mode="r", encoding="utf-8") as input_f:
                self.question_lib = json.loads(input_f.read())["data"]
                input_f.close()
        except FileNotFoundError:
            print("No question lib file found, please init the question library first.")
            exit(1)

    def ann_search(self, user_q, top_n):
        '''
        返回相似度排名前top_n的问题以及答案
        返回格式为
        [(question1, similarity1, answer1), (question2, similarity2, answer2), ... (questionn, similarityn, answern)]
        '''
        user_q_vec = self.sent2vec.Sent2Vec(user_q)
        similarity = []
        for qa_pair in self.question_lib:
            similarity.append(
                (
                    qa_pair['Q'], 
                    self.sent2vec.cosine_similarity(
                        user_q_vec, 
                        self.sent2vec.Sent2Vec(qa_pair['Q'])
                    ),
                    qa_pair['A']
                )
            )
        similarity.sort(key=lambda x: x[1], reverse=True)
        return similarity[:top_n]