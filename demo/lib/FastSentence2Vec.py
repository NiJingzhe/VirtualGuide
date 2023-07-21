import jieba.posseg as pseg
from gensim.models import Word2Vec as w2v
import numpy as np


class FastSentence2Vec(object):
    '''
    由于Word2Vec得到的是词语的向量，我们要求解句子的向量就需要一种方法根据词语的向量得到句子的向量。
    而采用的方法是对句子中词语向量的加权平均池化
    权重由词语的词性决定，并且存于self.factor中

    load(model_path) -> void 方法用于加载Word2Vec模型

    Sent2Vec(sent) -> np.array 方法用于将句子转换为向量

    cosine_similarity(vec1, vec2) -> float 方法用于计算两个向量的余弦相似度
    '''

    def __init__(self):
        self.model_loaded = False
        self.model = None
        self.factor = {
            'ns': 0.12,
            'nt': 0.15,
            'n': 0.15,
            's': 0.09,
            'f': 0.11,
            'v': 0.13,
            'ry': 0.11,
            'rys': 0.15,
            'ryt': 0.15,
            'ryv': 0.18,
            'other': 0.05
        }

    def load(self, model_path) -> None:
        self.model = w2v.load(model_path)
        self.model_loaded = True

    def Sent2Vec(self, sent) -> np.ndarray:
        if not self.model_loaded:
            raise Exception('Model not loaded')
        else:
            words_pos_pairs = [
                word_pos_pair for word_pos_pair in pseg.cut(sent)
            ]
            for word_pos_pair in words_pos_pairs:
                if list(word_pos_pair)[1] == 'x':
                    del words_pos_pairs[words_pos_pairs.index(word_pos_pair)]
            vec = np.zeros(
                np.shape(self.model.wv[list(words_pos_pairs[0])[0]])[0]
            )
            total_weight = 0
            for word_pos in words_pos_pairs:
                if list(word_pos)[1] in self.factor.keys():
                    vec = np.add(
                        vec, 
                        self.model.wv[list(word_pos)[0]] * self.factor[list(word_pos)[1]]
                    )
                    total_weight += self.factor[list(word_pos)[1]]
                else:
                    vec = np.add(
                        vec, 
                        self.model.wv[list(word_pos)[0]] * self.factor["other"]
                    )
                    total_weight += self.factor["other"]
            return np.divide(vec, total_weight)

    def cosine_similarity(self, vec1, vec2) -> float:
        return np.dot(vec1, vec2)/(np.linalg.norm(vec1)*np.linalg.norm(vec2))
