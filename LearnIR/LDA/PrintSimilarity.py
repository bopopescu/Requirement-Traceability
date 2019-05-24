
import os

'''
 打印相似性
'''

def printSims(sourceArtifact, fileDictionary, sims):
    # 对相似性进行排序
    simsSorted = sorted(enumerate(sims), key=lambda item: -item[1])
    print(simsSorted)
    print(simsSorted[0:5])
    print(simsSorted[0][1])

    print("-----------")
    print("相似度大于0.1的源代码文件的Id：")
    for code in simsSorted:
        # 如果源代码文件的相似度大于0.1
        if code[1] > 0.1:
            # print(code)
            # 源代码文件的Id
            print(code[0])

    print("------------------------")
    print("相似性排名前5的link")
    # 选取相似性排名前5的link
    for code in simsSorted[:5]:
        useCaseFile = os.path.basename(sourceArtifact)
        codeId = code[0]
        codeSim = code[1]

        simList = useCaseFile + "\t" + fileDictionary[codeId] + "\t" + str(codeSim)

        print(simList)

    print("-------------------")
    print("相似性大于0.01的link：")
    # 选取相似性大于0.01的link
    for code in simsSorted:
        useCaseFile = os.path.basename(sourceArtifact)
        codeId = code[0]
        codeSim = code[1]

        if codeSim > 0.01:
            simLine = useCaseFile + "\t" + fileDictionary[codeId] + "\t" + str(codeSim)

            print(simLine)

def printSimsToFile(sourceArtifact, fileDictionary, simsSorted, outputSimFile):
    fo = open(outputSimFile, "a", encoding="UTF-8")

    # 对相似性进行排序
    # simsSorted = sorted(enumerate(sims), key=lambda item: -item[1])

    # fo.write(str(simsSorted)+"\n")
    # fo.write(str(simsSorted[0:5])+"\n")
    # fo.write(str(simsSorted[0][1])+"\n")

    # fo.write("-----------"+"\n")
    # fo.write("相似度大于0.1的源代码文件的Id："+"\n")
    # for code in simsSorted:
    #     # 如果源代码文件的相似度大于0.1
    #     if code[1] > 0.1:
    #         # print(code)
    #         # 源代码文件的Id
    #         fo.write(str(code[0])+"\n")

    # fo.write("------------------------"+"\n")
    # fo.write("相似性排名前5的link"+"\n")
    # 选取相似性排名前5的link
    # for code in simsSorted[:5]:
    #     useCaseFile = os.path.basename(sourceArtifact)
    #     codeId = code[0]
    #     codeSim = code[1]
    #
    #     simList = useCaseFile + "\t" + fileDictionary[codeId] + "\t" + str(codeSim)
    #
    #     fo.write(simList+"\n")
    #
    # fo.write("-------------------"+"\n")
    # fo.write("相似性大于0.01的link："+"\n")

    # 选取相似性大于0.1的link
    for code in simsSorted[:10]:
        useCaseFile = os.path.basename(sourceArtifact)
        codeId = code[0]
        codeSim = code[1]

        # if codeSim > 0.1:
        simLine = useCaseFile + "\t" + fileDictionary[codeId] + "\t" + str(codeSim)

        fo.write(simLine+"\n")
    fo.write("----------------------------------------------------------------------------------\n")
    fo.close()

def printSimsToFileByStep(useCaseFileDictionary, sourceCodeFileDictionary,
                         model, step, simsLinks, oracleList):
    if model == "TF-IDF":
        outputSimFile = "../../output/tfidfSimilarityStep"
    if model == "LDA":
        outputSimFile = "../../output/LDASimilarityStep"

    outputSimFile = outputSimFile+ str(step) + ".txt"

    # 清空一下输出文件
    fo = open(outputSimFile, "w", encoding="UTF-8")
    # fo.close()
    #
    # fo = open(outputSimFile, "a", encoding="UTF-8")
    # 存放当前的UseCaseId
    changeSignId = 0
    # 存放当前的UseCaseId对应的记录数
    recordCount = 0
    for pair in simsLinks:
        useCaseId = pair[0]
        codeId = pair[1]
        codeSim = pair[2]
        # 换到一下个新的UseCase
        if changeSignId != useCaseId:
            # 更改当前的UseCaseId
            changeSignId = useCaseId
            # 将记录数归零
            recordCount = 0

        recordCount += 1
        if recordCount > 10:
            continue

        simLine = useCaseFileDictionary[useCaseId] + "\t" + \
                  sourceCodeFileDictionary[codeId] + "\t" + str(codeSim)
        simPair = (useCaseId, codeId)
        if simPair in oracleList:
            simLine = simLine+"\t\t"+"[##]"
        fo.write(simLine+"\n")

        if recordCount == 10:
            fo.write("----------------------------------------------------------------------------------\n")

    fo.close()

# 记录不同阶段oracleList的相似度
def printOracleSim(useCaseFileDictionary, sourceCodeFileDictionary,
                         model, step, simsLinks, oracleList):
    if model == "TF-IDF":
        outputSimFile = "../../output/tfidfOracleSimStep"
    if model == "LDA":
        outputSimFile = "../../output/LDAOracleSimStep"

    outputSimFile = outputSimFile+ str(step) + ".txt"

    # 清空一下输出文件
    fo = open(outputSimFile, "w", encoding="UTF-8")
    # fo.close()
    #
    # fo = open(outputSimFile, "a", encoding="UTF-8")

    for pair in oracleList:
        useCaseId = pair[0]
        codeId = pair[1]
        for simPair in simsLinks:
            if simPair[0] == useCaseId and simPair[1] == codeId:
                codeSim = simPair[2]

        simLine = useCaseFileDictionary[useCaseId] + "\t" + \
                  sourceCodeFileDictionary[codeId] + "\t" + str(codeSim)
        fo.write(simLine+"\n")

    fo.close()

