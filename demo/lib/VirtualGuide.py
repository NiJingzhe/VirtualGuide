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

