#!/usr/bin/python
#-*-coding=utf-8-*-

import os
import math
import Use_TFIDF_Model
import Use_LDA_Model
import PrintSimilarity
import Result

# 依次读取所有的UseCase
def UseCase_Code_Text_Sim(dictionary, corpus, useCaseFileDictionary,
                          model, simsLinks):
    i = 0
    inputUseCaseDir = "E:/PyCharm/project/input/UseCase"
    # 设置输出结果文件
    # 使用TFIDF模型
    if model == "TF-IDF":
        outputSimFile = "../../output/tfidfSimilarityStep1.txt"
    # 使用LDA模型
    if model == "LDA":
        outputSimFile = "../../output/LDASimilarityStep1.txt"

    # 清空一下输出文件
    fo = open(outputSimFile, "w", encoding="UTF-8")
    fo.close()

    for root, dirs, files in os.walk(inputUseCaseDir):
        for file in files:
            # UseCase文件为UTF-8编码
            # foRead = open(os.path.join(root, file), "r", encoding="UTF-8")
            # print(foRead.name+ "   "+os.path.join(root, file))
            # print(str(file))
            # if str(file) == "UC1.txt" or str(file) == "UC2.txt":
            sourceArtifact = os.path.join(root, file)

            # 使用TFIDF模型
            if model == "TF-IDF":
                sims = Use_TFIDF_Model.useTFIDFModel(sourceArtifact, dictionary, corpus)

            # 使用LDA模型
            if model == "LDA":
                sims = Use_LDA_Model.useLDAModel(sourceArtifact, dictionary, corpus)

            # 对相似性进行排序
            simsSorted = sorted(enumerate(sims), key=lambda item: -item[1])

            # 将文件相似性Link输出到文件
            # PrintSimilarity.printSimsToFile(sourceArtifact, sourceCodeFileDictionary, simsSorted, outputSimFile)

            # 文件相似性List的item:(codeId, sim)-->[usecaseId, codeId, sim]
            recordSimilarity(useCaseId=i, simsSorted=simsSorted, simsLinks=simsLinks)

            file_full_name = str(file)
            index = file_full_name.rfind(".")
            file_simple_name = file_full_name[:index]
            useCaseFileDictionary[i] = file_simple_name
            i += 1


# 根据源代码的结构信息更新相似度
def sourceCodeBetweenSimilarity(sourceCodeFileDictionary, useCaseFileDictionary, dictionary, corpus,
                                simsLinks, NodeList, model, threshold):
    # print("----------------------------------------")
    # print("simsLinks=", simsLinks)

    # 设置sim变化输出结果文件
    if model == "TF-IDF":
        outputSimFile = "../../output/tfidfSimChangeStep2.txt"
    # 使用LDA模型
    if model == "LDA":
        outputSimFile = "../../output/LDASimChangeStep2.txt"

    # 清空一下输出文件
    fo = open(outputSimFile, "w", encoding="UTF-8")
    fo.close()

    changeCount = 0
    simsLinksOriginal = []
    for simPair in simsLinks:
        simsLinksOriginal.append(tuple(simPair))

    for simPair in simsLinksOriginal:
        d = simPair[0]
        Ci = simPair[1]
        similarity_d_Ci = simPair[2]

        # 确定(d, Ci)
        if similarity_d_Ci > threshold:
            for nodePair in NodeList:
                # 确定(Ci, Cj)
                if Ci == nodePair[0]:
                    Cj = nodePair[1]
                    # 返回Sim(Ci, Cj)文本相似度
                    if model == "TF-IDF":
                        similarity_Ci_Cj = Use_TFIDF_Model.getCodeTextSim(Ci, Cj, dictionary, corpus)
                    if model == "LDA":
                        similarity_Ci_Cj = Use_LDA_Model.getCodeTextSim(Ci, Cj, dictionary, corpus)

                    # 返回dist(Ci, Cj)
                    distance = getNodeDistance(Ci, Cj)

                    # 搜索得到Sim(d,Cj)
                    # similarity_d_Cj = getDocToCodeSim(d, Cj, simsLinksOriginal)
                    # 重新计算Sim(d,Cj)
                    # similarity_d_Cj = similarity_d_Cj + (similarity_Ci_Cj/distance)

                    # 更新simsLinks
                    updateSimsLinks(sourceCodeFileDictionary, useCaseFileDictionary,
                                    d, Cj, simsLinks, similarity_Ci_Cj, distance, model)
                    changeCount = changeCount + 1

                elif Ci == nodePair[1]:
                    Cj = nodePair[0]
                    # 返回Sim(Ci, Cj)文本相似度
                    if model == "TF-IDF":
                        similarity_Ci_Cj = Use_TFIDF_Model.getCodeTextSim(Ci, Cj, dictionary, corpus)

                    if model == "LDA":
                        similarity_Ci_Cj = Use_LDA_Model.getCodeTextSim(Ci, Cj, dictionary, corpus)

                    # 返回dist(Ci, Cj)
                    distance = getNodeDistance(Ci, Cj)
                    # 更新simsLinks
                    updateSimsLinks(sourceCodeFileDictionary, useCaseFileDictionary,
                                    d, Cj, simsLinks, similarity_Ci_Cj, distance, model)
                    changeCount = changeCount + 1

    print("changeCount=", changeCount)

    # print("simsLinksOriginal=", simsLinksOriginal)
    # print("simsLinksOriginal length=", len(simsLinksOriginal))
    # print("simsLinks", simsLinks)
    # print("simsLinks length=", len(simsLinks))
    # print("----------------------------------------")
    # return simsLinks


def recordSimilarity(useCaseId, simsSorted, simsLinks):

    # 对相似性进行排序
    # simsSorted = sorted(enumerate(sims), key=lambda item: -item[1])

    # 选取相似性大于0.1的link
    for code in simsSorted:
        codeId = code[0]
        codeSim = code[1]

        # if codeSim > 0.1:
        #     simLine = [useCaseId, codeId, codeSim]
        #     ListSimilarity.append(simLine)
        simLine = [useCaseId, codeId, codeSim]
        simsLinks.append(simLine)


# 读取Node边关系文件
def recordNodeEdge(NodeList):
    nodeFile = "../../input/eTOUR/Embedding/linkCount1.txt"
    fo = open(nodeFile, "r", encoding="UTF-8")
    for line in fo:
        line = line.replace("\n", "")
        nodeLine = line.split(" ")
        node1 = int(nodeLine[0])
        node2 = int(nodeLine[1])
        edge = (node1, node2)
        NodeList.append(edge)

# 获取两个节点之间的欧氏距离
def getNodeDistance(node1, node2):
    embeddingFile = "../../input/eTOUR/Embedding/embedding1.txt"
    fo = open(embeddingFile, "r", encoding="UTF-8")
    vector1 = []
    vector2 = []
    # print("node1=", node1)
    # print("node2=", node2)
    for line in fo:
        line = line.replace("\n", "")
        nodeLine = line.split(" ")
        nodeId = int(nodeLine[0])
        # print("nodeId=", nodeId)
        if nodeId == node1:
            vector1 = nodeLine[1:len(nodeLine)-1]
        if nodeId == node2:
            vector2 = nodeLine[1:len(nodeLine)-1]
        if len(vector1)>0 and len(vector2)>0:
            break

    # print("vector1 length=", len(vector1))
    # print("vector1=", vector1)
    # print("vector2 length=", len(vector2))
    # print("vector2=", vector2)
    # if len(vector2) < 20:
    #     print("(", node1, ",", node2, ")")
    #     print("vector2=", vector2)
    sum = 0
    for index in range(len(vector1)):
        temp = float(vector1[index]) - float(vector2[index])
        temp = pow(temp, 2)
        sum = sum + temp

    distance = math.sqrt(sum)
    return distance

    # print("vector1 length=", len(vector1))
    # print("vector1=", vector1)
    # print("vector2=", vector2)

# 更新simsLinks
def updateSimsLinks(sourceCodeFileDictionary, useCaseFileDictionary,
                    d, Cj, simsLinks, similarity_Ci_Cj, distance, model):
    if model == "TF-IDF":
        outputSimFile = "../../output/tfidfSimChangeStep2.txt"
    # 使用LDA模型
    if model == "LDA":
        outputSimFile = "../../output/LDASimChangeStep2.txt"

    fo = open(outputSimFile, "a", encoding="UTF-8")
    # sim = -1
    for simPair in simsLinks:
        if d == simPair[0] and Cj == simPair[1]:
            # sim = simPair[2]
            # sim = sim + (similarity_Ci_Cj/distance)
            # print("before sim =(", d, ",", Cj, ",", simPair[2], ")")

            changeLine = "("+useCaseFileDictionary[d]+", "+sourceCodeFileDictionary[Cj]+")  sim="+str(simPair[2])+" --> "
            simPair[2] = simPair[2] + (similarity_Ci_Cj/(distance+1))*10
            # print("after sim=(", d, ",", Cj, ",", simPair[2], ")")
            changeLine = changeLine+str(simPair[2])+"\n"
            fo.write(changeLine)
            break

    fo.close()
    # simsLinks[1][2] = 10


def recordOracle(oracleList, sourceCodeFileDictionary, useCaseFileDictionary):
    fo = open("E:/PyCharm/project/input/eTOUR/eTour_oracle.txt", "r", encoding="UTF-8")
    for line in fo:

        # 预处理行文本
        index = len(line)-1
        line = line[:index]

        pairLine = line.split(" ")

        useCase = pairLine[0]
        codeList = pairLine[1:]

        useCaseId = getUseCaseId(useCase, useCaseFileDictionary)

        for codeName in codeList:
            codeId = getCodeId(codeName, sourceCodeFileDictionary)
            if useCaseId != -1 and codeId != -1:
                link = (useCaseId, codeId)
                oracleList.append(link)

def getUseCaseId(useCaseName, useCaseFileDictionary):
    # useCaseId默认为-1
    useCaseId = -1
    for index in range(len(useCaseFileDictionary)):
        if useCaseFileDictionary[index] == useCaseName:
            useCaseId = index
            break

    return useCaseId

def getCodeId(codeName, sourceCodeFileDictionary):
    # codeId默认为-1
    codeId = -1
    for index in range(len(sourceCodeFileDictionary)):
        if sourceCodeFileDictionary[index] == codeName:
            codeId = index
            break

    return codeId


# 过滤link，得到最终结果
def filterLink(simsLinks, finalLinks, threshold):
    for candidateLink in simsLinks:
        useCaseId = candidateLink[0]
        codeId = candidateLink[1]
        similarity = candidateLink[2]

        # 筛选条件，比如设置阈值
        if similarity > threshold:
            link = (useCaseId, codeId)
            finalLinks.append(link)

# 合并LinkList，得到最终的finalLinks
def mergeLinkList(finalLinks, *modelFinalList):
    for list in modelFinalList:
        for pair in list:
            if pair not in finalLinks:
                finalLinks.append(pair)


# 得到最终结果中正确的链接
def getCorrectLinks(finalLinks, oracleList, myCorrectLinks):
    for myLink in finalLinks:
        if myLink in oracleList:
            myCorrectLinks.append(myLink)

# 分别获得每种模型的结果
def get_eachModel_CorrectLinks(myCorrectLinks, tfidf_finalLinks, lda_finalLinks, result_statistics):
    tfidf_only_correct = []
    lda_only_correct = []
    common_correct = []
    for pair in myCorrectLinks:
        if (pair in tfidf_finalLinks) and (pair not in lda_finalLinks):
            tfidf_only_correct.append(pair)

    for pair in myCorrectLinks:
        if (pair not in tfidf_finalLinks) and (pair in lda_finalLinks):
            lda_only_correct.append(pair)

    for pair in myCorrectLinks:
        if (pair in tfidf_finalLinks) and (pair in lda_finalLinks):
            common_correct.append(pair)

    print("length=", len(tfidf_only_correct), "\ttfidf_only_correct=", tfidf_only_correct)
    print("length=", len(lda_only_correct), "\tlda_only_correct=", lda_only_correct)
    print("length=", len(common_correct), "\tcommon_correct=", common_correct)
    Result.lengthChange("tfidf_only_correct", result_statistics, tfidf_only_correct)
    Result.lengthChange("lda_only_correct", result_statistics, lda_only_correct)
    Result.lengthChange("common_correct", result_statistics, common_correct)


# 获得准确率
def getPrecision(myCorrectLinks, finalLinks):
    correctNumber = len(myCorrectLinks)
    foundNumber = len(finalLinks)

    precision = correctNumber/foundNumber

    return precision

# 获得召回率
def getRecall(myCorrectLinks, oracleList):
    correctNumber = len(myCorrectLinks)
    oracleNumber = len(oracleList)

    recall = correctNumber/oracleNumber

    return recall
