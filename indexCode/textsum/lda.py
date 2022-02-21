"""

2.生成文本摘要

"""


import gensim
import jieba
import numpy as np
import config
import re

class LDASummarizer():
    def __init__(self):
        # cws_model_path = os.path.join(config['development'].LTP_DATA_DIR, 'cws.model')
        # self.segmentor = Segmentor()
        # self.segmentor.load(cws_model_path)
        #self.model = gensim.models.ldamodel.LdaModel.load(config['development'].LDA_PATH)
        self.model = gensim.models.ldamodel.LdaModel.load("textsum/models/lda.model")

        self.stopwords = []
        #with open(config['development'].STOPWORDS_PATH, 'r',encoding="utf-8") as f:
        with open("textsum/chinese_stopwords.txt", 'r', encoding="utf-8") as f:
            for line in f.readlines():
                word = line.split('\n')[0]
                self.stopwords.append(word)
        self.dictionary = gensim.corpora.Dictionary.load_from_text("textsum/dictionary")
    
    def sent_tokenizer(self, text):
        """将原始文本拆分为句子"""
        # sents = SentenceSplitter.split(text)
        # return [sent for sent in sents if sent]
        sentence_txt = []
        pattern = r"([，。？！…\s]+)"  # 正则匹配模式,用+表示至少一个字符
        pattern2 = re.compile(r'[^\u4e00-\u9fa5]') #清除文本内所有非中文
        #flags = ["，", "。", "？", "！", "…", "……"," "]
        # with open(text, "r", encoding="utf-8") as reader_file:
        #     for line in reader_file:  # 一行就是一篇文章
        #         spilt_list = re.split(pattern=pattern, string=line)
        #         segment = ""
        #         for segment_i in spilt_list:
        #             segment += segment_i
        #             if segment_i in flags:
        #                 # 去除分割子句中的空格,\n,\t等符号,并加上"\r"回车符换行
        #                 sentence_txt.append("".join(segment.split()) + "\r")
        #                 segment = ""
        #         sentence_txt.append("\r")
        spilt_list = re.split(pattern=pattern, string=text)
        #print(spilt_list)
        segment = ""
        for segment_i in spilt_list:
            chinese = re.sub(pattern2,"",segment_i)
            if(len(chinese)>=1):
                sentence_txt.append(chinese)
            #segment += segment_i
            #if segment_i in flags:
                # 去除分割子句中的空格,\n,\t等符号,并加上"\r"回车符换行
            #    sentence_txt.append("".join(segment.split()) + "\r")
            #    segment = ""
        #print(sentence_txt)
        return sentence_txt
    
    def sents2wordlist(self, sents):
        #sents = jieba.lcut(sents)
        #print(sents)
        sents = [[w for w in jieba.cut(line,cut_all=True) if
                  w not in self.stopwords and w.isprintable() and w not in "‘’“”，、；。？！《》（）//" and
                  w in self.dictionary.values()]
                 for line in sents]
        #print(sents)
        return sents
    
    def wordlist2vec(self, wordlist):
        vecs = []
        for sent in wordlist:
            bow = self.dictionary.doc2bow(sent)
            vec = self.model.inference([bow])
            vecs.append(vec[0])
        return np.concatenate(vecs)

    def doc2vec(self, wordlist):
        doc = [w for sent in wordlist for w in sent]
        bow = self.dictionary.doc2bow(doc)
        vec = self.model.inference([bow])
        return vec[0]

    
    def summarize(self, text):
        sents = self.sent_tokenizer(text)
        if len(sents)<2:
            sents = ['错误']
        wordlist = self.sents2wordlist(sents)
        sents_vec = self.wordlist2vec(wordlist)
        doc_vec = self.doc2vec(wordlist)
        ranks = np.matmul(doc_vec, sents_vec.T)[0]
        ranked_sentences = sorted([(ranks[i], s) for i, s in enumerate(sents)],
                                  reverse=True)
        # self.segmentor.release()
        print(ranked_sentences)
        return ranked_sentences

# if __name__ == '__main__':
#     text = "中国共产党是人民的政党，是先锋队"
#     print(LDASummarizer().summarize(text))