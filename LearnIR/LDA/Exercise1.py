#!/usr/bin/python
#-*-coding=utf-8-*-

# import os
# for root,dirs,files in os.walk("E:\PyCharm\project\input\\UseCase"):
 # for dir in dirs:
 #  print os.path.join(root,dir).decode('gbk').encode('utf-8');
 # for file in files:
  # print(os.path.join(root, file))

# files = ["UC1.TXT", "UC2.TXT"]
'''
 1.读取SouceCode，选取一个UseCase，计算该UseCase与所有源代码的文本相似性,
    得到与该UseCase文本相似性较高的SourceCode
'''

import MyUtil

import os

# 记录所有的文档的单词
documents = []
inputSourceCodeDir = "E:/PyCharm/project/input/SourceCode"

# 为每个源代码文件分配一个Id并记录到文件
fileDictionary = {}
i = 0
# foWrite = open("E:/PyCharm/project/output/SourceCodeFile_Id.txt", "w")
# 读取所有的源代码文件
for root,dirs,files in os.walk(inputSourceCodeDir):
    for file in files:
        # 源代码文件为UTF-8编码
        foRead = open(os.path.join(root, file), "r", encoding="UTF-8")
        content = foRead.read()
        documents.append(content)
        fileDictionary[i] = str(file)
        # 将源代码文件及其对应的Id记录到文件
        # foWrite.write(str(file)+" "+str(i)+"\n")
        i += 1

foRead.close()
# foWrite.close()
print(fileDictionary)
#print(documents[26])

'''
# ========================================
# 文本预处理

"""预处理(easy_install nltk)"""

#引入nltk
import nltk

#分词
from nltk.corpus import brown
texts_lower = [[word for word in document.lower().split()] for document in documents]
from nltk.tokenize import word_tokenize
texts_tokenized = [[word.lower() for word in word_tokenize(document)] for document in documents]

#去除停用词
from nltk.corpus import stopwords
english_stopwords = stopwords.words('english')
texts_filtered_stopwords = [[word for word in document if not word in english_stopwords] for document in texts_tokenized]

#去除标点符号
english_punctuations = [',', '.', ':', ';', '?', '(', ')', '[', ']', '&',
                        '!', '=', '*', '@', '#', '$', '%', '/', '\\', '+',
                        '>', '<', '\'\'', '``', '_-', '**', '-', '==', '***', '|']
texts_filtered1 = [[word for word in document if not word in english_punctuations] for document in texts_filtered_stopwords]
# 去除整数
# texts_filtered2 = [[word for word in document if not word.isdigit()] for document in texts_filtered1]
# print("isNumber="+str(MyUtil.isNumber("0.1")))
# 去除浮点数
# texts_filtered = [[word for word in document if not MyUtil.isNumber(word)] for document in texts_filtered2]
texts_filtered = [[word for word in document if not MyUtil.is_number(word)] for document in texts_filtered1]

#词干化
from nltk.stem.lancaster import LancasterStemmer
st = LancasterStemmer()
texts_stemmed = [[st.stem(word) for word in docment] for docment in texts_filtered]


#去除过低频词
all_stems = sum(texts_stemmed, [])
stems_once = set(stem for stem in set(all_stems) if all_stems.count(stem) == 1)
texts = [[stem for stem in text if stem not in stems_once] for text in texts_stemmed]

# ========================================
'''
import TextPreprocess
texts = TextPreprocess.textProprocess(documents=documents)

#print("length="+str(len(documents)))
#print(documents[20])

from gensim import corpora, models, similarities

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

dictionary = corpora.Dictionary(texts)
dictionary.save('../../tmp/SourceCode.dict')  # store the dictionary,for future reference

print(dictionary)
print(dictionary.token2id)
# print(dictionary.token2id.get("actor"))

corpus = [dictionary.doc2bow(text) for text in texts]
corpora.MmCorpus.serialize('../../tmp/SourceCode.mm', corpus)  # store to dist,for later use
# pprint(corpus)


'''
# set tfidf model
tfidf = models.TfidfModel(corpus)

featureNum = len(dictionary.token2id.keys())
index = similarities.SparseMatrixSimilarity(tfidf[corpus], num_features=featureNum)

#源文件(UseCase)
# UseCase为iso-8859-1编码
sourceArtifact = "E:/PyCharm/project/input/UseCase/UC2.TXT"
fo = open(sourceArtifact, "r", encoding="iso-8859-1")
new_doc = fo.read()
# the word 'interaction' does not appear in the dictionary and is ignored
new_vec = dictionary.doc2bow(new_doc.lower().split())
print(new_vec)
ml_tfidf = tfidf[new_vec]

sims = index[ml_tfidf]

'''

sourceArtifact = "E:/PyCharm/project/input/UseCase/UC2.TXT"
# 使用TFIDF模型
import Use_TFIDF_Model
sims = Use_TFIDF_Model.useTFIDFModel(sourceArtifact=sourceArtifact, dictionary=dictionary, corpus=corpus)

# 使用LDA模型
# import Use_LDA_Model
# sims = Use_LDA_Model.useLDAModel(sourceArtifact=sourceArtifact, dictionary=dictionary, corpus=corpus)

print("===================")
# print(sims)

#打印文件相似性Link
import PrintSimilarity
PrintSimilarity.printSims(sourceArtifact=sourceArtifact, fileDictionary=fileDictionary, sims=sims)

'''
# 对相似性进行排序
simsSorted = sorted(enumerate(sims), key=lambda item: -item[1])
print(simsSorted)
print(simsSorted[0:5])
print(simsSorted[0][1])

print("-----------")

for code in simsSorted:
    # 如果源代码文件的相似度大于0.1
    if code[1]>0.1:
        # print(code)
        # 源代码文件的Id
        print(code[0])

print("------------------------")
#选取相似性排名前5的link
for code in simsSorted[:5]:
    useCaseFile = os.path.basename(sourceArtifact)
    codeId = code[0]
    codeSim = code[1]

    simList = useCaseFile + "\t" + fileDictionary[codeId] + "\t" + str(codeSim)

    print(simList)

print("-------------------")
#选取相似性大于0.01的link
for code in simsSorted:
    useCaseFile = os.path.basename(sourceArtifact)
    codeId = code[0]
    codeSim = code[1]

    if codeSim > 0.01:
        simList = useCaseFile + "\t" + fileDictionary[codeId] + "\t" + str(codeSim)

        print(simList)


'''

# fo.close()

# 打开文件

# for file in files:
#     fo = open("../../input/"+file, "r", encoding="iso-8859-1")
#     content = fo.read()
#     documents.append(content)
#
# print(documents[0])

# 关闭文件
# fo.close()