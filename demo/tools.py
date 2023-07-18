from lib.PreTrainer import Word2VecPreTrain
from lib.TrainDataPreProcesser import PreProcesser
from lib.ZhihuSpyder import ZhihuSpyder
from QASNet import QASNet
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
        qas_net = QASNet(model_path, input_file_path)
        
        user_q = input("Please input your question: ")
        while user_q != "exit":
            print("-------------------------------------------------")
            print("top 3 questions and answers:")
            for q_v_a in qas_net.ann_search(user_q, 3):
                print("\nquestion: ",q_v_a[0], "\nanswer: ",q_v_a[2], "\nsimilariry: ", q_v_a[1])
            print("-------------------------------------------------")
            user_q = input("Please input your question: ")
            