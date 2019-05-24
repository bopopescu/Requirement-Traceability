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
import Result

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

# preprocessFinishTime = time.clock()
# print("preprocess consume Time = ", "%.2f" % (preprocessFinishTime-beginTime), "s")

print("Step 1 : -----------------------------------------------------------------------")
# Step 1: 计算UseCase与每个源代码的文本相似度

# 将link记录到一个list里，每个元素为三元组[usecaseId, codeId, sim]
tfidf_simsLinks = []
lda_simsLinks=[]

model = "TF-IDF"
ComputeSimilarity.UseCase_Code_Text_Sim(dictionary, corpus, useCaseFileDictionary,
                          model, tfidf_simsLinks)
# tfidf_step1_FinishTime = time.clock()
# print("tfidf_step1 consume Time = ", "%.2f" % (tfidf_step1_FinishTime-preprocessFinishTime), "s")

model = "LDA"
ComputeSimilarity.UseCase_Code_Text_Sim(dictionary, corpus, useCaseFileDictionary,
                          model, lda_simsLinks)
# lda_step1_FinishTime = time.clock()
# print("lda_step1 consume Time = ", "%.2f" % (lda_step1_FinishTime-tfidf_step1_FinishTime), "s")

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


# 获得只使用文本信息的结果
result_statistics = {}
print("Only Textual Result:")
Result.getResult(tfidf_simsLinks, lda_simsLinks, oracleList, result_statistics, [])
print()
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

threshold = []
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
# tfidf_step2_FinishTime = time.clock()
# print("tfidf_step2 consume Time = ", "%.2f" % (tfidf_step2_FinishTime-lda_step1_FinishTime), "s")

model = "LDA"
# LDA的阈值
lda_threshold = 0.8
threshold.append((tfidf_threshold, lda_threshold))
ComputeSimilarity.sourceCodeBetweenSimilarity(sourceCodeFileDictionary, useCaseFileDictionary, dictionary, corpus,
                                              lda_simsLinks, NodeList, model, lda_threshold)
# 将文件相似性Link输出到文件
PrintSimilarity.printSimsToFileByStep(useCaseFileDictionary, sourceCodeFileDictionary,
                                     model, 2, lda_simsLinks, oracleList)
PrintSimilarity.printOracleSim(useCaseFileDictionary, sourceCodeFileDictionary,
                         model, 2, lda_simsLinks, oracleList)
print("tfidf_threshold =", tfidf_threshold, "\tlda_threshold =", lda_threshold)
# lda_step2_FinishTime = time.clock()
# print("lda_step2 consume Time = ", "%.2f" % (lda_step2_FinishTime-tfidf_step2_FinishTime), "s")

print("tfidf_simsLinks=", tfidf_simsLinks)

# 获得综合使用文本信息和结构信息的结果
print("Textual and Structural Result:")
Result.getResult(tfidf_simsLinks, lda_simsLinks, oracleList, result_statistics, threshold)

print("result_statistics=\t", result_statistics)
Result.print_statistics(result_statistics, threshold)

endTime = time.clock()
print("total Time=", "%.2f" % (endTime - beginTime), "s")
print("total Time=", "%.2f" % ((endTime - beginTime) / 60), "min")
