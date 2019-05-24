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
import PrintSimilarity

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

# 文本预处理
import TextPreprocess
texts = TextPreprocess.textProprocessSimple(documents=documents)

from pprint import pprint
#pprint(texts)

# 得到dictionary
dictionary = corpora.Dictionary(texts)
dictionary.save('../../tmp/SourceCode.dict')  # store the dictionary,for future reference

# 得到corpus
corpus = [dictionary.doc2bow(text) for text in texts]
corpora.MmCorpus.serialize('../../tmp/SourceCode.mm', corpus)  # store to dist,for later use

# 为每个UseCase文件分配一个Id并记录到文件
useCaseFileDictionary = {}

preprocessFinishTime = time.clock()
print("preprocess consume Time = ", "%.2f" % (preprocessFinishTime-beginTime), "s")

print("Step 1 : -----------------------------------------------------------------------")
# Step 1: 计算UseCase与每个源代码的文本相似度

# 将link记录到一个list里，每个元素为三元组[usecaseId, codeId, sim]
tfidf_simsLinks = []
lda_simsLinks=[]

model = "TF-IDF"
ComputeSimilarity.UseCase_Code_Text_Sim(dictionary, corpus, useCaseFileDictionary,
                          model, tfidf_simsLinks)
tfidf_step1_FinishTime = time.clock()
print("tfidf_step1 consume Time = ", "%.2f" % (tfidf_step1_FinishTime-preprocessFinishTime), "s")

model = "LDA"
ComputeSimilarity.UseCase_Code_Text_Sim(dictionary, corpus, useCaseFileDictionary,
                          model, lda_simsLinks)
lda_step1_FinishTime = time.clock()
print("lda_step1 consume Time = ", "%.2f" % (lda_step1_FinishTime-tfidf_step1_FinishTime), "s")

# oracleList每个元素为二元组(usecaseId, codeId)
oracleList = []
ComputeSimilarity.recordOracle(oracleList, sourceCodeFileDictionary, useCaseFileDictionary)
print("length=", len(oracleList), "   ", "oracleList=", oracleList)

# 将文件相似性Link输出到文件
model = "TF-IDF"
PrintSimilarity.printSimsToFileByStep(useCaseFileDictionary, sourceCodeFileDictionary,
                                     model, 1, tfidf_simsLinks, oracleList)
PrintSimilarity.printOracleSim(useCaseFileDictionary, sourceCodeFileDictionary,
                         model, 1, tfidf_simsLinks, oracleList)
model = "LDA"
PrintSimilarity.printSimsToFileByStep(useCaseFileDictionary, sourceCodeFileDictionary,
                                     model, 1, lda_simsLinks, oracleList)
PrintSimilarity.printOracleSim(useCaseFileDictionary, sourceCodeFileDictionary,
                         model, 1, lda_simsLinks, oracleList)

print("Step 2 : -----------------------------------------------------------------------")
# Step 2: 根据源代码之间的结构信息更新相似度

# 读取Node边关系文件
NodeList = []
ComputeSimilarity.recordNodeEdge(NodeList)

print("tfidf_simsLinks=", tfidf_simsLinks)
# print("begin")
# testTime = time.clock()
# print("Test Time = ", testTime, "s")

# 根据源代码的结构信息更新相似度

model = "TF-IDF"
# tfidf的阈值
tfidf_threshold = 0.1
ComputeSimilarity.sourceCodeBetweenSimilarity(sourceCodeFileDictionary, useCaseFileDictionary, dictionary, corpus,
                                              tfidf_simsLinks, NodeList, model, tfidf_threshold)
# 将文件相似性Link输出到文件
PrintSimilarity.printSimsToFileByStep(useCaseFileDictionary, sourceCodeFileDictionary,
                                     model, 2, tfidf_simsLinks, oracleList)
PrintSimilarity.printOracleSim(useCaseFileDictionary, sourceCodeFileDictionary,
                         model, 2, tfidf_simsLinks, oracleList)
tfidf_step2_FinishTime = time.clock()
print("tfidf_step2 consume Time = ", "%.2f" % (tfidf_step2_FinishTime-lda_step1_FinishTime), "s")

model = "LDA"
# LDA的阈值
lda_threshold = 0.95
ComputeSimilarity.sourceCodeBetweenSimilarity(sourceCodeFileDictionary, useCaseFileDictionary, dictionary, corpus,
                                              lda_simsLinks, NodeList, model, lda_threshold)
# 将文件相似性Link输出到文件
PrintSimilarity.printSimsToFileByStep(useCaseFileDictionary, sourceCodeFileDictionary,
                                     model, 2, lda_simsLinks, oracleList)
PrintSimilarity.printOracleSim(useCaseFileDictionary, sourceCodeFileDictionary,
                         model, 2, lda_simsLinks, oracleList)
lda_step2_FinishTime = time.clock()
print("lda_step2 consume Time = ", "%.2f" % (lda_step2_FinishTime-tfidf_step2_FinishTime), "s")

print("tfidf_simsLinks=", tfidf_simsLinks)

print("Step 3 : -----------------------------------------------------------------------")
# Step 3: 筛选出最终的link

# 最终的linkList，每个元素为二元组(usecaseId, codeId)
finalLinks = []
tfidf_finalLinks = []
lda_finalLinks = []

# 筛选出最终的linkList结果
# TF-IDF
# tfidf的阈值
tfidf_threshold = 0.1
ComputeSimilarity.filterLink(tfidf_simsLinks, tfidf_finalLinks, tfidf_threshold)
print("length=", len(tfidf_finalLinks), "\t", "tfidf_finalLinks=", tfidf_finalLinks)

# LDA
# LDA的阈值
lda_threshold = 0.9
ComputeSimilarity.filterLink(lda_simsLinks, lda_finalLinks, lda_threshold)
print("length=", len(lda_finalLinks), "\t", "lda_finalLinks=", lda_finalLinks)

# 合并结果
ComputeSimilarity.mergeLinkList(finalLinks, tfidf_finalLinks, lda_finalLinks)
print("length=", len(finalLinks), "\t", "finalLinks=", finalLinks)

filter_FinishTime = time.clock()
print("filter consume Time = ", "%.2f" % (filter_FinishTime-lda_step2_FinishTime), "s")

print("Step 4 : -----------------------------------------------------------------------")
# Step 4: 获得结果

# 获得结果中正确的link
# TF-IDF
tfidf_CorrectLinks = []
ComputeSimilarity.getCorrectLinks(tfidf_finalLinks, oracleList, tfidf_CorrectLinks)
print("length=", len(tfidf_CorrectLinks), "   ", "tfidf_CorrectLinks=", tfidf_CorrectLinks)

# LDA
lda_CorrectLinks = []
ComputeSimilarity.getCorrectLinks(lda_finalLinks, oracleList, lda_CorrectLinks)
print("length=", len(lda_CorrectLinks), "   ", "lda_CorrectLinks=", lda_CorrectLinks)

# 总体
myCorrectLinks = []
ComputeSimilarity.getCorrectLinks(finalLinks, oracleList, myCorrectLinks)
print("length=", len(myCorrectLinks), "   ", "myCorrectLinks=", myCorrectLinks)

# 返回准确率

# TF-IDF
tfidf_precision = ComputeSimilarity.getPrecision(tfidf_CorrectLinks, tfidf_finalLinks)
print("tfidf_precision=", tfidf_precision)
# LDA
lad_precision = ComputeSimilarity.getPrecision(lda_CorrectLinks, lda_finalLinks)
print("lad_precision=", lad_precision)
# 总体
precision = ComputeSimilarity.getPrecision(myCorrectLinks, finalLinks)
print("precision=", precision)

# 返回召回率

# TF-IDF
tfidf_recall = ComputeSimilarity.getRecall(tfidf_CorrectLinks, oracleList)
print("tfidf_recall=", tfidf_recall)
# LDA
lad_recall = ComputeSimilarity.getRecall(lda_CorrectLinks, oracleList)
print("lad_recall=", lad_recall)
# 总体
recall = ComputeSimilarity.getRecall(myCorrectLinks, oracleList)
print("recall=", recall)

# 分别获得每种模型的结果
ComputeSimilarity.get_eachModel_CorrectLinks(myCorrectLinks, tfidf_finalLinks, lda_finalLinks)

endTime = time.clock()
# print("beginTime=", beginTime)
# print("endTime=", endTime)
print("total Time=", "%.2f" % (endTime-beginTime), "s")
print("total Time=", "%.2f" % ((endTime-beginTime)/60), "min")
