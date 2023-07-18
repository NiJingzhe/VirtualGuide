'''
这是Word2Vec的预训练类，用于训练词向量模型
'''
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence

class Word2VecPreTrain(object):
    def __init__(self, train_data, model_save_path):
        self.input_file = train_data
        self.output_file = model_save_path

    def train(self, model_path = ''):
        if model_path != '':
            model = Word2Vec.load(model_path)
            model.build_vocab(LineSentence(self.input_file), update=True)
            model.train(LineSentence(self.input_file), total_examples=model.corpus_count, epochs=model.epochs)
        else:
            model = Word2Vec(LineSentence(self.input_file), vector_size=150, window=5, min_count=5, workers=8)
            
        model.save(self.output_file)
        model.wv.save_word2vec_format(self.output_file + '.bin', binary=True)
