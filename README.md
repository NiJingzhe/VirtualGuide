# Virtual Guide Project
---
>首先，预训练模型和训练相关语料库可以在这个链接里找到
>
>[一个OneDrive链接](https://zjueducn-my.sharepoint.com/:f:/r/personal/nijingzhe_zju_edu_cn/Documents/VirtualGuideModel?csf=1&web=1&e=F8y596)

## 一、如何使用？

### tools.py 脚本

- tools脚本主要会跟着几个参数：
  
  - `--mode`：可选值：`train, test, preprocess, grab`

    - 下面分别说明四个模式下的其余参数含义

    - `grab`:
    
      - `--input-file-path`：需要抓取的主题，如`train_data`中的`grab_topic.txt`，一行一个主题

      - `--output-file-path`：抓取的知乎文章存储在这个路径对应的文件下

    - `preprocess`:
      
      - `--input-file-path`：需要预处理（即分词，繁体化简体等）的语料文本文件，如`grab`模式下抓取的知乎文章文件
  
      - `--output-file-path`：预处理后的语料文本文件，一般命名为`xxx.seg`表示已经完成分词的文件
      
      - `--data-type`：输入的语料类型，因为不同的语料可能需要不同的预处理，针对现状我们有`zhihu`和`zhwiki`两种类型，分别对应知乎和维基百科的语料，所以该参数二选一，默认为`zhihu`

    - `train`:
    
      - `--input-file-path`：需要训练的语料文本文件，如`preprocess`模式下预处理后的语料文本文件
      
      - `--model-path`：可能该训练是在已经训练好的模型上的增量训练，那么该参数表示一个预训练模型的路径，**不设置则默认从头开始训练新模型** 
      
      - `--output-file-path`：训练好的模型存储在这个路径对应的文件下

    - `test`:
    
      - `--model-path`：测试时选择加载的模型路径
      
      - `--input-file-path`：测试时的输入文件，一般是`test_data`中的`data.json`这样的`Q&A`对，用于构建本地问题库

    **一个使用tools脚本的实际例子**

    ```powershell
    PS D:\Proj\VirtualGuide\demo> python .\tools.py --mode=train --input-file-path=./train_data/zhihu.seg --model-path=./model/zhwiki.model --output-file-path=./model/zhwiki.model
    ```


