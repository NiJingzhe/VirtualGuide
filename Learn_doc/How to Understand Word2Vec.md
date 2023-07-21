# *How to Understand Word2Vec*
---

## **I. What is a Language Model ?**
 
  - The concept of language model is extremely wide and can be applied to any sequence of data. In the context of NLP, there are still may types of language model which are able to handle different tasks. However the most common LM is the one that predicts the next word in a sequence of words, which make the returned text become more natural and fluent.
  
  - Generally speaking, there are two types of LM: **Statistical LM** and **Neural LM**. Statistical LM is based on the probability of a word given the previous words, while Neural LM is based on the neural network.
  
## **II. Take a Look at "N-gram" Statistical LM**

  - If we want to predict the probability of a word given the previous words, we can use the chain rule of probability to calculate it:
  $$
    p(w_t|w_1,w_2,..., w_n) = p(w_1)p(w_2|w_1)p(w_3|w_1, w_2)...p(w_t|w_1,w_2,...,w_{t-1})
  $$

  - Now we suppose that the probability of a word only depends on the previous $n$ words (usually smaller than 5), which means that the probability of a word given the previous words can be written as:
  $$
        p(w_t|w_1,w_2,..., w_{t-1}) = p(w_t|w_{t-n-1},w_{t-n},...,w_{t-1})
  $$

  - So, if we can calculate the possibility of a word given the previous $n$ words, we can calculate the probability of a sentence by multiplying the probability of each word given the previous $n$ words. However, the number of parameters in this model is too large to be trained. For example, if we have a vocabulary of 10000 words, and we want to predict the next word given the previous 4 words, we need to train $10000^4$ parameters, which is impossible. So $n$ usually is below 3, which determined that the model is not able to capture the long-term dependency between words.

## **III. Take a Look at Neural LM**

  - Of course, as its name said, this kind of LM is based on Neural Network.