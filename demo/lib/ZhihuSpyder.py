from duckduckgo_search import DDGS 
from bs4 import BeautifulSoup as bs
import requests


class ZhihuSpyder(object):
    def __init__(self):
        self.history_herf = []

    def grab_topic_to_file(self, topic, file_path):
        with DDGS(proxies="socks5://localhost:7890", timeout=20) as ddgs:
            total_artical = ''
            for result in ddgs.text(topic):
                herf = result['href']
                if herf.startswith('https://zhuanlan.zhihu.com/') and herf not in self.history_herf:
                    #接下来向herf发起请求
                    print(herf)
                    response = requests.get(herf)
                    soup = bs(response.text, 'lxml')
                    artical = ''
                    #class_这么写的原因可以到知乎专栏里通过浏览器控制台查看他的页面结构
                    for div in soup.find_all(name = 'div', attrs={'class' : "RichText ztext Post-RichText css-1g0fqss"}):
                        artical += div.text
                    print(artical, '\n')
                    print('---------------------------------------------')
                    total_artical += artical
                    self.history_herf.append(herf)
            
            #把已经抓取的内容读出来，加上新的一并写入文件
            try:
                with open(file_path, mode="r", encoding="utf-8") as input_f:
                    total_artical = input_f.read() + total_artical
                    input_f.close()                                                                            
            except FileNotFoundError:
                print("No train data file found, will now create one.")
                open(file_path, mode="w", encoding="utf-8").close()
            
            with open(file_path, mode="w", encoding="utf-8") as output_f:
                output_f.write(total_artical)
                output_f.close()

    def clear_history_herf(self):
        self.history_herf = []
