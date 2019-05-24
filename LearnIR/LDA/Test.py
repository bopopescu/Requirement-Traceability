#!/usr/bin/python
#-*-coding=utf-8-*-

import ComputeSimilarity
# ComputeSimilarity.recordOracle()

# NodeList = []
# ComputeSimilarity.recordNodeEdge(NodeList)
#
# print("NodeList length=", len(NodeList))
# print("NodeList=", NodeList)

# node1 = "5"
# node2 = "25"
# distance = ComputeSimilarity.getNodeDistance(node1, node2)
# print(node1, node2, "distance=", distance)


def changeLink(simsLinks):
    # simlinsChange = []
    # simlinsChange = simsLinks[0:]
    simsLinks[1][2] = 10
    # simlinsChange[1][2] = 10
    # return simlinsChange


def sourceCodeBetweenSimilarity(simsLinks):
    # simlinsChange = simsLinks
    # simlinsOriginal = tuple(simsLinks)

    simlinsOriginal = []
    print("simsLinks=", simsLinks)
    # simlinsOriginal.append([-1, -1, 100])
    for simPair in simsLinks:
        simlinsOriginal.append(tuple(simPair))

    # simlinsOriginal.append([-1, -1, 100])
    changeLink(simsLinks)
    # print("simlinsOriginal=", changeLink(simsLinks))
    # print("simlinsOriginal=", simlinsChange)
    print("simsLinks=", simsLinks)
    print("simlinsOriginal=", simlinsOriginal)

