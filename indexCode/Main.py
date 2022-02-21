"""
封装代码
"""

import os
import sys
import pandas as pd
import cluster.single_pass_cluster as cluster
import textsum.lda as summary
from textrank4zh import TextRank4Keyword

class MyIndexCode():
    def __init__(self,filePath):
        #源文件路径
        self.filePath = filePath
        #1.聚类模型
        self.clusterModel = cluster.SinglePassCluster(max_features=100,simi_threshold=0.1)
        #2.摘要模型
        self.summaryModel = summary.LDASummarizer()
        #3.主题词模型
        self.keywordModel = TextRank4Keyword()

    #流程封装
    def run(self):
        if not os.path.exists(self.filePath):
            print("源文件 {} 不存在".format(self.filePath))
            sys.exit(-1)
        # 1.聚类
        # {'0':[0,1,2],'1':[3,4,5]}
        clustMap = self.clusterModel.single_pass(self.filePath)
        print("正在运行中，忽略上述警告信息...")
        # 2.按照各个类别对文章进行摘要和获取关键词
        keywords = []
        keyphrase = []
        bigsummary = ""
        file = pd.read_excel(self.filePath)
        for key in clustMap.keys():
            #获得各类的文章索引
            textIndexs = clustMap.get(key)
            #按照索引读取文章，进行摘要
            bigtext = ""
            for index in textIndexs:
                text = file.iloc[index,1]
                #text = text.replace(" ",",")
                text = str(text) + "。"
                bigtext += text
                #print("++++")
                #print(index)
                #print(text)
                #print("++++")
                #摘要
            summary = self.summaryModel.summarize(bigtext)
            #print(type(summary))
            #选择最重要中的两句话拼接
            #if summary == "ERROR":
            #    continue
            #print(len(summary))
            if len(summary)>1:
                summary = summary[0][1] + summary[1][1]
            elif len(summary)!=0:
                summary = summary[0][1]# + summary[1][1]
            #print(type(summary))
            #print(summary)
            if(summary!="错误"):
                bigsummary += summary+","
            #print(bigsummary)
        self.keywordModel.analyze(text=bigsummary,lower=True, window=3, pagerank_config={'alpha':0.85})
        keywords = self.keywordModel.get_keywords(30, word_min_len=2)
        keyphrase = self.keywordModel.get_keyphrases(keywords_num=20, min_occur_num = 0)
        #print(keyphrase)
        #print(keywords)
        return (keyphrase,keywords)

if __name__ == '__main__':
    #参数为输入文件路径
    model = MyIndexCode('docs/3600主题公园1.xlsx')
    keyphrse,keyword = model.run()
    print("_________结果__________")
    print(keyphrse)
    print(keyword)