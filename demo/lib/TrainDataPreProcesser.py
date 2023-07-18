'''
该脚本负责预处理训练语料，根据训练语料的种类不同，可以选择不同的预处理方式
1. 中文维基百科语料
2. 来自知乎专栏的文章语料
最终我们会根据预处理器的初始化参数生成对应语料库分词后的.seg文件
'''
from gensim.corpora import WikiCorpus
from opencc import OpenCC
import jieba
import re

class ZhWikiPreProcesser(object):

    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file

    def convert_xml_to_text(self, input_file, output_file):
        with open(output_file, mode='w', encoding='utf-8') as output_f:
            index = 0
            space = ' '
            wiki = WikiCorpus(input_file, dictionary=[])
            for text in wiki.get_texts():
                output_f.write(space.join(text) + '\n')
                index += 1
                if index % 10000 == 0:
                    print('Saved ' + str(index) + ' articles...')

    
    def convert_trad_to_simp(self, input_file, output_file):
        with open(output_file, mode='w', encoding='utf-8') as output_f:
            with open(input_file, mode='r', encoding='utf-8') as input_f:
                index = 0
                cc = OpenCC('t2s')
                for line in input_f:
                    line = cc.convert(line.strip())
                    output_f.write(line+'\n')
                    index += 1

                    if index % 10000 == 0:
                        print('Converted ' + str(index) + ' articles...')

    def text_segement(self, input_file, output_file):
        with open(output_file, mode='w', encoding='utf-8') as output_f:
            with open(input_file, mode='r', encoding='utf-8') as input_f:
                index = 0
                for line in input_f:
                    line = jieba.cut(line.strip())
                    output_f.write(' '.join(line) + '\n')
                    index += 1

                    if index % 10000 == 0:
                        print('Segmented ' + str(index) + ' articles...')

    def pre_processer(self):
        self.convert_xml_to_text(self.input_file, self.input_file+'.text')
        self.convert_trad_to_simp(self.input_file+'.text', self.input_file+'.simp')
        self.text_segement(self.input_file+'.simp', self.output_file)

class zhihuPreProcesser(object):
    
        def __init__(self, input_file, output_file):
            self.input_file = input_file
            self.output_file = output_file
            self.stop_words = ['，','。','；','（','）','【','】','？','！','《','》','、','|','“','”','：','(',')','[',']','\\','/']

        def keep_chinese(self, text):
            """
            去除文本中的非汉字字符，只保留汉字内容。
            """
            chinese_pattern = re.compile(r'[^\u4e00-\u9fa5]')  # 匹配非汉字字符的正则表达式
            chinese_text = chinese_pattern.sub('', text)  # 用空字符替换非汉字字符
            return chinese_text

        def split_sentences(self, input_file, output_file):
            with open(output_file, mode="w", encoding="utf-8") as output_f:
                with open(input_file, mode="r", encoding="utf-8") as input_f:
                    index = 0
                    for line in input_f:
                        sentences = line.strip().split("。")
                        for sentence in sentences:
                            sentence_ = sentence
                            sentence_ = self.keep_chinese(sentence_)
                            output_f.write(sentence_.strip()+"\n")
                        index += 1
                        if index % 10000 == 0:
                            print('Split ' + str(index) + ' sentences...')
    
        def text_segement(self, input_file, output_file):
            with open(output_file, mode='w', encoding='utf-8') as output_f:
                with open(input_file, mode='r', encoding='utf-8') as input_f:
                    index = 0
                    for line in input_f:
                        line = [word for word in jieba.cut(line.strip()) if word not in self.stop_words]
                        output_f.write(' '.join(line) + '\n')
                        index += 1
    
                        if index % 10000 == 0:
                            print('Segmented ' + str(index) + '  sentences...')
    
        def pre_processer(self):
            self.split_sentences(self.input_file, self.input_file+'.text')
            self.text_segement(self.input_file+'.text', self.output_file)

class PreProcesser(object):

    def __init__(self, input_file, output_file, data_type = 'zhihu'):
        '''
        初始化时决定使用哪种预处理器，即通过data_type参数决定，可以选择的参数有：
        1. zhihu
        2. zhwiki
        '''
        self.data_type = data_type
        self.input_file = input_file
        self.output_file = output_file

    def pre_processer(self):
        if self.data_type == 'zhihu':
            zhihuPreProcesser(self.input_file, self.output_file).pre_processer()
        elif self.data_type == 'zhwiki': 
            ZhWikiPreProcesser(self.input_file, self.output_file).pre_processer()