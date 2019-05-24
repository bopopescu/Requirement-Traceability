# -*- coding: utf-8 -*-
import time,re,os,sys,math

# 统计关键词及个数
def CountKey(fileName):
    try:
        # 计算文件行数
        lineNums = len(open(fileName, 'r').readlines())
        print("lineCount=", lineNums)
        # 统计格式 格式<Key:Value> <属性:出现个数>
        i = 0
        table = {}
        source = open(fileName, "r")
        while i < lineNums:
            line = source.readline()
            line = line.rstrip('\n')
            words = line.split(" ")  # 空格分隔
            # 字典插入与赋值
            for word in words:
                if word != "" and word in table:  # 如果存在次数加1
                    num = table[word]
                    table[word] = num + 1
                elif word != "":  # 否则初值为1
                    table[word] = 1
            i = i + 1
        # 键值从大到小排序 函数原型：sorted(dic,value,reverse)
        dic = sorted(table.items(), key=lambda asd: asd[1], reverse=True)
        return dic
    except Exception as e:
        print('Error:', e)
    finally:
        source.close()

# 统计关键词及个数 并计算相似度
def MergeKeys(dic1, dic2):
    # 合并关键词 采用三个数组实现
    arrayKey = []
    for i in range(len(dic1)):
        arrayKey.append(dic1[i][0])  # 向数组中添加元素
    for i in range(len(dic2)):
        if dic2[i][0] in arrayKey:
            # print('has_key', dic2[i][0])
            pass
        else:  # 合并
            arrayKey.append(dic2[i][0])
    # 计算词频 infobox可忽略TF-IDF
    arrayNum1 = [0] * len(arrayKey)
    arrayNum2 = [0] * len(arrayKey)
    # 赋值arrayNum1
    for i in range(len(dic1)):
        key = dic1[i][0]
        value = dic1[i][1]
        j = 0
        while j < len(arrayKey):
            if key == arrayKey[j]:
                arrayNum1[j] = value
                break
            else:
                j = j + 1
    # 赋值arrayNum2
    for i in range(len(dic2)):
        key = dic2[i][0]
        value = dic2[i][1]
        j = 0
        while j < len(arrayKey):
            if key == arrayKey[j]:
                arrayNum2[j] = value
                break
            else:
                j = j + 1
    print('arrayNum1:',arrayNum1)
    print('arrayNum2:',arrayNum2)
    # 计算两个向量的点积,计算两个向量的模
    x = 0
    i = 0
    sq1 = 0
    sq2 = 0
    while i < len(arrayKey):
        x = x + arrayNum1[i] * arrayNum2[i]
        sq1 = sq1 + arrayNum1[i] * arrayNum1[i]  # pow(a,2)
        sq2 = sq2 + arrayNum2[i] * arrayNum2[i]
        i = i + 1
    result = float(x) / (math.sqrt(sq1) * math.sqrt(sq2))
    return result

'''
------------------------------------------------------- 
基本步骤：
    1.分别统计两个文档的关键词
    2.两篇文章的关键词合并成一个集合,相同的合并,不同的添加
    3.计算每篇文章对于这个集合的词的词频 TF-IDF算法计算权重
    4.生成两篇文章各自的词频向量
    5.计算两个向量的余弦相似度,值越大表示越相似                             
------------------------------------------------------- 
'''
# 主函数
def main():
    # 计算文档1的关键词及个数
    fileName1 = "../DataSet/UseCase1.TXT"
    dic1 = CountKey(fileName1)
    # 计算文档2的关键词及个数
    fileName2 = "../DataSet/UseCase2.txt"
    dic2 = CountKey(fileName2)
    # 合并两篇文章的关键词及相似度计算
    result = MergeKeys(dic1, dic2)
    print("similarity=")
    print(result)

if __name__ == '__main__':
    main()
