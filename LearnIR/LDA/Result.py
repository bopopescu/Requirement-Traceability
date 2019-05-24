#!/usr/bin/python
#-*-coding=utf-8-*-

import os

import ComputeSimilarity
import time

import Use_LDA_Model

def getResult(tfidf_simsLinks, lda_simsLinks, oracleList, result_statistics, threshold):
    print("Step 3 : -----------------------------------------------------------------------")
    # Step 3: 筛选出最终的link

    # 最终的linkList，每个元素为二元组(usecaseId, codeId)
    finalLinks = []
    tfidf_finalLinks = []
    lda_finalLinks = []

    # 筛选出最终的linkList结果
    # TF-IDF
    # tfidf的阈值
    tfidf_threshold = 0.05
    ComputeSimilarity.filterLink(tfidf_simsLinks, tfidf_finalLinks, tfidf_threshold)
    print("length=", len(tfidf_finalLinks), "\t", "tfidf_finalLinks=", tfidf_finalLinks)
    lengthChange("tfidf_finalLinks", result_statistics, tfidf_finalLinks)

    # LDA
    # LDA的阈值
    lda_threshold = 0.8
    threshold.append((tfidf_threshold, lda_threshold))
    ComputeSimilarity.filterLink(lda_simsLinks, lda_finalLinks, lda_threshold)
    print("length=", len(lda_finalLinks), "\t", "lda_finalLinks=", lda_finalLinks)
    lengthChange("lda_finalLinks", result_statistics, lda_finalLinks)

    print("tfidf_threshold =", tfidf_threshold, "\tlda_threshold =", lda_threshold)

    # 合并结果
    ComputeSimilarity.mergeLinkList(finalLinks, tfidf_finalLinks, lda_finalLinks)
    print("length=", len(finalLinks), "\t", "finalLinks=", finalLinks)
    lengthChange("finalLinks", result_statistics, finalLinks)

    filter_FinishTime = time.clock()
    # print("filter consume Time = ", "%.2f" % (filter_FinishTime - lda_step2_FinishTime), "s")

    # print("Step 4 : -----------------------------------------------------------------------")
    # Step 4: 获得结果

    # 获得结果中正确的link
    # TF-IDF
    tfidf_CorrectLinks = []
    ComputeSimilarity.getCorrectLinks(tfidf_finalLinks, oracleList, tfidf_CorrectLinks)
    print("length=", len(tfidf_CorrectLinks), "\t", "tfidf_CorrectLinks=", tfidf_CorrectLinks)
    lengthChange("tfidf_CorrectLinks", result_statistics, tfidf_CorrectLinks)

    # LDA
    lda_CorrectLinks = []
    ComputeSimilarity.getCorrectLinks(lda_finalLinks, oracleList, lda_CorrectLinks)
    print("length=", len(lda_CorrectLinks), "\t", "lda_CorrectLinks=", lda_CorrectLinks)
    lengthChange("lda_CorrectLinks", result_statistics, lda_CorrectLinks)

    # 总体
    myCorrectLinks = []
    ComputeSimilarity.getCorrectLinks(finalLinks, oracleList, myCorrectLinks)
    print("length=", len(myCorrectLinks), "\t", "myCorrectLinks=", myCorrectLinks)
    lengthChange("myCorrectLinks", result_statistics, myCorrectLinks)

    # 返回准确率

    # TF-IDF
    tfidf_precision = ComputeSimilarity.getPrecision(tfidf_CorrectLinks, tfidf_finalLinks)
    print("tfidf_precision=\t", tfidf_precision)
    numberChange("tfidf_precision", result_statistics, tfidf_precision)
    # LDA
    lda_precision = ComputeSimilarity.getPrecision(lda_CorrectLinks, lda_finalLinks)
    print("lda_precision=\t", lda_precision)
    numberChange("lda_precision", result_statistics, lda_precision)
    # 总体
    precision = ComputeSimilarity.getPrecision(myCorrectLinks, finalLinks)
    print("precision\t=", precision)
    numberChange("precision", result_statistics, precision)

    # 返回召回率

    # TF-IDF
    tfidf_recall = ComputeSimilarity.getRecall(tfidf_CorrectLinks, oracleList)
    print("tfidf_recall=\t", tfidf_recall)
    numberChange("tfidf_recall", result_statistics, tfidf_recall)
    # LDA
    lda_recall = ComputeSimilarity.getRecall(lda_CorrectLinks, oracleList)
    print("lda_recall=\t", lda_recall)
    numberChange("lda_recall", result_statistics, lda_recall)
    # 总体
    recall = ComputeSimilarity.getRecall(myCorrectLinks, oracleList)
    print("recall=\t", recall)
    numberChange("recall", result_statistics, recall)

    # 分别获得每种模型的结果
    ComputeSimilarity.get_eachModel_CorrectLinks(myCorrectLinks, tfidf_finalLinks, lda_finalLinks,
                                                 result_statistics)

    # endTime = time.clock()
    # print("beginTime=", beginTime)
    # print("endTime=", endTime)
    # print("total Time=", "%.2f" % (endTime - beginTime), "s")
    # print("total Time=", "%.2f" % ((endTime - beginTime) / 60), "min")

def lengthChange(key, result_statistics, list):
    if key not in result_statistics:
        result_statistics[key] = [len(list)]
    else:
        result_statistics[key].append(len(list))


def numberChange(key, result_statistics, number):
    if key not in result_statistics:
        result_statistics[key] = [number]
    else:
        result_statistics[key].append(number)

def print_statistics(result_statistics, threshold):
    outputFile = "../../output/StatisticsResult.txt"
    fo = open(outputFile, "w", encoding="UTF-8")
    line = "tfidf_threshold="+str(threshold[0][0])+"-----"+str(threshold[1][0])+"\n"
    fo.write(line)
    line = "lda_threshold="+str(threshold[0][1])+"-----"+str(threshold[1][1])+"\n"
    fo.write(line)
    topic_num = Use_LDA_Model.getTopicNum()
    line = "topic_num="+str(topic_num)+"\n"
    fo.write(line)

    line = ""
    for key in result_statistics.keys():
        line += key+"\t"
        line += str(result_statistics[key][0])+"\t=====>\t"+str(result_statistics[key][1])
        line += "\n"

    fo.write(line)
    fo.close()
