#!/usr/bin/python
#-*-coding=utf-8-*-

'''
 1.读取SouceCode，选取一个UseCase，计算该UseCase与所有源代码的文本相似性,
    得到与该UseCase文本相似性较高的SourceCode
'''

import os
from gensim import corpora, models, similarities

import ComputeSimilarity
import Use_TFIDF_Model
import Use_LDA_Model

import time

beginTime = time.clock()

# 记录所有的文档的单词
documents = []
inputSourceCodeDir = "E:/PyCharm/project/input/SourceCode"

# 为每个源代码文件分配一个Id并记录到文件
sourceCodeFileDictionary = {}
i = 0
# 读取所有的源代码文件
for root,dirs,files in os.walk(inputSourceCodeDir):
    for file in files:
        # 源代码文件为UTF-8编码
        foRead = open(os.path.join(root, file), "r", encoding="UTF-8")
        content = foRead.read()
        documents.append(content)
        file_full_name = str(file)
        index = file_full_name.rfind(".")
        file_simple_name = file_full_name[:index]
        sourceCodeFileDictionary[i] = file_simple_name
        i += 1
        foRead.close()

# print("sourceCodeFileDictionary=   " + str(sourceCodeFileDictionary))
#print(documents[26])

# 文本预处理
import TextPreprocess
texts = TextPreprocess.textProprocessSimple(documents=documents)

# print(texts)

#print("length="+str(len(documents)))
#print(documents[20])

# remove commen words and tokenize
# stoplist = set('for a of the and to in'.split())
# texts = [[word for word in document.lower().split() if word not in stoplist]
#          for document in documents]

# remove words that appear only once
# from collections import defaultdict
#
# frequency = defaultdict(int)
# for text in texts:
#     for token in text:
#         frequency[token] += 1
#
# texts = [[token for token in text if frequency[token] > 1]
#          for text in texts]

from pprint import pprint

#pprint(texts)

# 得到dictionary
dictionary = corpora.Dictionary(texts)
dictionary.save('../../tmp/SourceCode.dict')  # store the dictionary,for future reference

# print(dictionary)
# print(dictionary.token2id)
# print(dictionary.token2id['valu'])
# print(dictionary.token2id.get("valu"))

# 得到corpus
corpus = [dictionary.doc2bow(text) for text in texts]
corpora.MmCorpus.serialize('../../tmp/SourceCode.mm', corpus)  # store to dist,for later use
# pprint(corpus)
# CodeTextSim = Use_TFIDF_Model.getCodeTextSim(1, 23, dictionary, corpus)
# print("Ci Cj CodeTextSim=", CodeTextSim)


# 将link记录到一个list里，每个元素为三元组[usecaseId, codeId, sim]
simsLinks = []

# 为每个UseCase文件分配一个Id并记录到文件
useCaseFileDictionary = {}
i = 0
# 设置输出结果文件
similarityFile = "E:/PyCharm/project/output/Similarity1.txt"
# 清空一下输出文件
fo = open("E:/PyCharm/project/output/Similarity1.txt", "w", encoding="UTF-8")
fo.close()

# Step 1: 计算UseCase与每个源代码的文本相似度  

# 依次读取所有的UseCase
inputUseCaseDir = "E:/PyCharm/project/input/UseCase"
for root,dirs,files in os.walk(inputUseCaseDir):
    for file in files:
        # UseCase文件为UTF-8编码
        # foRead = open(os.path.join(root, file), "r", encoding="UTF-8")
        # print(foRead.name+ "   "+os.path.join(root, file))
        # print(str(file))
        # if str(file) == "UC1.txt" or str(file) == "UC2.txt":
            sourceArtifact = os.path.join(root, file)
            # 使用TFIDF模型
            # sims = Use_TFIDF_Model.useTFIDFModel(sourceArtifact, dictionary, corpus)

            # 使用LDA模型
            sims = Use_LDA_Model.useLDAModel(sourceArtifact, dictionary, corpus)

            # print("====================================================")

            # 对相似性进行排序
            simsSorted = sorted(enumerate(sims), key=lambda item: -item[1])

            # 打印文件相似性Link
            import PrintSimilarity
            # PrintSimilarity.printSims(sourceArtifact=sourceArtifact, fileDictionary=sourceCodeFileDictionary, sims=sims)
            PrintSimilarity.printSimsToFile(sourceArtifact=sourceArtifact, fileDictionary=sourceCodeFileDictionary, simsSorted=simsSorted)

            # 记录文件相似性
            ComputeSimilarity.recordSimilarity(useCaseId=i, simsSorted=simsSorted, simsLinks=simsLinks)


            file_full_name = str(file)
            index = file_full_name.rfind(".")
            file_simple_name = file_full_name[:index]
            useCaseFileDictionary[i] = file_simple_name
            i += 1

        # foRead.close()


# print(str(ListSimilarity))
# print("simsLinks=   " + str(simsLinks))
# print("simsLinks length=   " + str(len(simsLinks)))


# Step 2: 根据源代码之间的结构信息更新相似度

# 读取Node边关系文件
NodeList = []
ComputeSimilarity.recordNodeEdge(NodeList)

print("simsLinks=", simsLinks)
print("begin")
# import Test
# Test.sourceCodeBetweenSimilarity(simsLinks)

# 根据源代码的结构信息更新相似度
ComputeSimilarity.sourceCodeBetweenSimilarity(dictionary, corpus, simsLinks, NodeList)

# 输出ListSimilarity到文件，可以筛选link
# print("useCaseFileDictionary=   " + str(useCaseFileDictionary))


# Step 3: 筛选出最终的link

# 最终的linkList，每个元素为二元组(usecaseId, codeId)
finalLinks = []
# 筛选出最终的linkList结果
ComputeSimilarity.filterLink(simsLinks, finalLinks)
print("length=", len(finalLinks), "   ", "finalLinks=", finalLinks)

# Step 4: 获得结果

# oracleList每个元素为二元组(usecaseId, codeId)
oracleList = []
ComputeSimilarity.recordOracle(oracleList, sourceCodeFileDictionary, useCaseFileDictionary)
print("length=", len(oracleList), "   ", "oracleList=", oracleList)

# 获得结果中正确的link
myCorrectLinks = []
ComputeSimilarity.getCorrectLinks(finalLinks, oracleList, myCorrectLinks)
print("length=", len(myCorrectLinks), "   ", "myCorrectLinks=", myCorrectLinks)

# 返回准确率
precision = ComputeSimilarity.getPrecision(finalLinks, myCorrectLinks)
print("precision=", precision)

# 返回召回率
recall = ComputeSimilarity.getRecall(oracleList, myCorrectLinks)
print("recall=", recall)

endTime = time.clock()
print("beginTime=", beginTime)
print("endTime=", endTime)
print("Time=", endTime-beginTime, "s")
