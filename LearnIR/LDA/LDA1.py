from gensim import corpora, models, similarities
import jieba

# 分词函数，返回分词列表
def cut(sentence):
    generator = jieba.cut(sentence)
    return [word for word in generator]


# 文本集和搜索词
text1 = open('../../input/UC1.TXT', encoding='ISO-8859-1').read()
text2 = open('../../input/UC2.TXT', encoding='ISO-8859-1').read()

texts = [text1, text2]
keyword = open('../../input/UC1.TXT', encoding='ISO-8859-1').read()
# 1、将【文本集】生成【分词列表】
texts = [cut(text) for text in texts]
# 2、基于文本集建立【词典】，并提取词典特征数
dictionary = corpora.Dictionary(texts)
feature_cnt = len(dictionary.token2id.keys())
# 3、基于词典，将【分词列表集】转换成【稀疏向量集】，称作【语料库】
corpus = [dictionary.doc2bow(text) for text in texts]
# 4、使用【TF-IDF模型】处理语料库
tfidf = models.TfidfModel(corpus)
# 5、同理，用【词典】把【搜索词】也转换为【稀疏向量】
kw_vector = dictionary.doc2bow(cut(keyword))
# 6、对【稀疏向量集】建立【索引】
index = similarities.SparseMatrixSimilarity(tfidf[corpus], num_features=feature_cnt)
# 7、相似度计算
sim = index[tfidf[kw_vector]]
for i in range(len(sim)):
    print('keyword 与 text%d 相似度为：%.2f' % (i+1, sim[i]))
