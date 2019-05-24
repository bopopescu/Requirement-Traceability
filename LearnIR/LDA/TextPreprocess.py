
import nltk
from nltk.corpus import brown

import MyUtil

'''
文本预处理

'''

# 处理原始文本
def textProprocess(documents):
    # 文本预处理

    # 引入nltk

    # 分词
    # texts_lower = [[word for word in document.lower().split()] for document in documents]
    # print("texts_lower" + str(texts_lower))
    from nltk.tokenize import word_tokenize
    texts_tokenized = [[word.lower() for word in word_tokenize(document)] for document in documents]

    # 去除停用词
    from nltk.corpus import stopwords
    english_stopwords = stopwords.words('english')
    texts_filtered_stopwords = [[word for word in document if not word in english_stopwords] for document in
                                texts_tokenized]

    # 去除标点符号
    english_punctuations = [',', '.', ':', ';', '?', '(', ')', '[', ']', '&',
                            '!', '=', '*', '@', '#', '$', '%', '/', '\\', '+',
                            '>', '<', '\'\'', '``', '_-', '**', '-', '==', '***', '|']
    texts_filtered1 = [[word for word in document if not word in english_punctuations] for document in
                       texts_filtered_stopwords]
    # 去除整数
    # texts_filtered2 = [[word for word in document if not word.isdigit()] for document in texts_filtered1]
    # print("isNumber="+str(MyUtil.isNumber("0.1")))
    # 去除浮点数
    # texts_filtered = [[word for word in document if not MyUtil.isNumber(word)] for document in texts_filtered2]
    texts_filtered = [[word for word in document if not MyUtil.is_number(word)] for document in texts_filtered1]

    # 词干化
    from nltk.stem.lancaster import LancasterStemmer
    st = LancasterStemmer()
    texts_stemmed = [[st.stem(word) for word in docment] for docment in texts_filtered]

    # 去除过低频词
    all_stems = sum(texts_stemmed, [])
    stems_once = set(stem for stem in set(all_stems) if all_stems.count(stem) == 1)
    texts = [[stem for stem in text if stem not in stems_once] for text in texts_stemmed]

    return texts


# 处理已经与处理过的文本，输入文本是用空格分隔的单词
def textProprocessSimple(documents):

    # 直接用空格切分单词
    # texts = [[word for word in document.split()] for document in documents]

    # from nltk.corpus import stopwords
    # english_stopwords = stopwords.words('english')
    #
    # print("---------------------------------------------------------")
    # print("english_stopwords = stopwords.words('english')")
    # print(english_stopwords)
    # print("---------------------------------------------------------")

    stopwords_list = []
    stopwords_file = "E:/PyCharm/project/input/StopWords/stopwords_Full.txt"
    foRead = open(stopwords_file, "r", encoding="ISO-8859-1")
    for line in foRead:
        line = line.replace("\n", "")
        stopwords_list.append(line)
    # line = foRead.readline()
    # while line:
    #     stopwords_list.append(line.replace("\n", ""))
    #     line = foRead.readline()
    foRead.close()
    # print("stopwords_list Full : "+str(stopwords_list))
    # print("stopwords_list Full lengrh = " + str(len(stopwords_list)))

    # 给每个单词设置一个token
    from nltk.tokenize import word_tokenize
    # texts_tokenized = [[word.lower() for word in word_tokenize(document)] for document in texts]
    texts_tokenized = [[word for word in word_tokenize(document)] for document in documents]

    # 去除停用词

    from nltk.corpus import stopwords
    english_stopwords = stopwords.words('english')
    texts_filtered_stopwords_nltk = [[word for word in document if not word in english_stopwords] for document in
                                texts_tokenized]

    texts_filtered_stopwords = [[word for word in document if not word in stopwords_list] for document in
                                texts_filtered_stopwords_nltk]

    return texts_filtered_stopwords

# 处理已经与处理过的文本，输入文本是用空格分隔的单词
def textProprocessOneFile(document):

    # 直接用空格切分单词
    # texts = [[word for word in document.split()] for document in documents]

    stopwords_list = []
    stopwords_file = "E:/PyCharm/project/input/StopWords/stopwords_Full.txt"
    foRead = open(stopwords_file, "r", encoding="ISO-8859-1")
    for line in foRead:
        line = line.replace("\n", "")
        stopwords_list.append(line)
    # line = foRead.readline()
    # while line:
    #     stopwords_list.append(line.replace("\n", ""))
    #     line = foRead.readline()
    foRead.close()

    # 去除停用词

    from nltk.corpus import stopwords
    english_stopwords = stopwords.words('english')
    texts_filtered_stopwords_nltk = [word for word in document if not word in english_stopwords]

    texts_filtered_stopwords = [word for word in texts_filtered_stopwords_nltk if not word in stopwords_list]

    return texts_filtered_stopwords