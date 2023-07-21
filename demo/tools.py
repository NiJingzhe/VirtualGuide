from lib.PreTrainer import Word2VecPreTrain
from lib.TrainDataPreProcesser import PreProcesser
from lib.ZhihuSpyder import ZhihuSpyder
from lib.VirtualGuide import VirtualGuide

from sklearn.decomposition import PCA
from matplotlib import pyplot
import sys
import getopt

if __name__ == "__main__":
    opts, args = getopt.getopt(
        sys.argv[1:],
        "",
        [
            "mode=", "input-file-path=", "output-file-path=", "model-path=", "data-type="
        ]
    )

    mode = ""
    input_file_path = ""
    output_file_path = ""
    model_path = ""
    data_type = ""

    for op, value in opts:
        if op == "--mode":
            mode = value
        elif op == "--input-file-path":
            input_file_path = value
        elif op == "--output-file-path":
            output_file_path = value
        elif op == "--model-path":
            model_path = value
        elif op == "--data-type":
            if value != "zhihu" and value != "zhwiki":
                print("data-type must be zhihu or zhwiki")
                exit(1)
            data_type = value

    if mode == "grab":
        print("launching grab mode...")
        zhihu_spyder = ZhihuSpyder()
        with open(input_file_path, mode="r", encoding="utf-8") as input_f:
            index = 0
            for line in input_f:
                line = line.strip()
                zhihu_spyder.grab_topic_to_file(line, output_file_path)
                index += 1
                print("Grabed " + str(index) + " topics...")
            input_f.close()

    if mode == "train":
        print("launching train mode...")
        pre_train = Word2VecPreTrain(input_file_path, output_file_path)
        pre_train.train(model_path)

    if mode == "preprocess":
        print("launching preprocess mode...")
        if data_type == '':
            data_type = 'zhihu'
        pre_processer = PreProcesser(
            input_file_path, output_file_path, data_type
        )
        pre_processer.pre_processer()

    if mode == "test":
        print("launching test mode...")
        virtual_guide = VirtualGuide(model_path, input_file_path)
        print("embedding model loaded successfully.")
        print("ask your question:")
        user_q = virtual_guide.hear_question("./test_data/question.wav")
        print(user_q)
        while user_q != "exit" and user_q != "quit" and user_q != "退出":
            virtual_guide.answer(user_q)
            print("------------------------------------------")
            print("ask your question: ", end="")
            user_q = virtual_guide.hear_question("./test_data/question.wav")
            print(user_q)

    if mode == "visualize":
        print("launching visualize mode...")
        word_list_file = input_file_path
        import gensim.models.word2vec as w2v
        import matplotlib.pyplot as plt
        plt.rc("font", family='Microsoft YaHei')
        model = w2v.Word2Vec.load(model_path)
        print("model loaded successfully.")

        with open(word_list_file, mode="r", encoding="utf-8") as input_f:
            words = input_f.read().splitlines()
            input_f.close()

        vectors = [model.wv[word] for word in words]

        # 使用PCA对向量进行降维
        pca = PCA(n_components=3)
        pca_vectors = pca.fit_transform(vectors)
        print("PCA finished.")
        # 绘制降维后的向量
        plt.figure(figsize=(10, 10))
        plt.scatter(pca_vectors[:, 0], pca_vectors[:, 1])
        for i, word in enumerate(words):
            plt.annotate(word, xy=(pca_vectors[i, 0], pca_vectors[i, 1]))
        plt.show()
