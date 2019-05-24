
from gensim import corpora, models, similarities

topic_num = 30

def getTopicNum():
    return topic_num

def useLDAModel(sourceArtifact, dictionary, corpus):
    # print("topic_num =", topic_num)
    # set LDA model
    lda = models.LdaModel(corpus, id2word=dictionary, num_topics=topic_num)

    featureNum = len(dictionary.token2id.keys())
    index = similarities.SparseMatrixSimilarity(lda[corpus], num_features=featureNum)
    # index = similarities.MatrixSimilarity(lda[corpus])

    # 源文件(UseCase)
    # UseCase为iso-8859-1编码
    fo = open(sourceArtifact, "r", encoding="iso-8859-1")
    new_doc = fo.read()
    # the word 'interaction' does not appear in the dictionary and is ignored
    new_vec = dictionary.doc2bow(new_doc.lower().split())
    # print(new_vec)

    ml_lda = lda[new_vec]

    sims = index[ml_lda]

    return sims

def getCodeTextSim(Ci, Cj, dictionary, corpus):
    # set LDA model
    lda = models.LdaModel(corpus, id2word=dictionary, num_topics=topic_num)
    featureNum = len(dictionary.token2id.keys())
    index = similarities.SparseMatrixSimilarity(lda[corpus], num_features=featureNum)
    # index = similarities.MatrixSimilarity(lda[corpus])

    # print("corpus[Ci]=", corpus[Ci])
    # index = similarities.MatrixSimilarity()
    # index = similarities.SparseMatrixSimilarity(tfidf[corpus_Ci], num_features=featureNum)

    Ci_vector = corpus[Ci]
    ml_lda = lda[Ci_vector]

    sims = index[ml_lda]
    # print("Ci sims=", sims)
    sim_Ci_Cj = sims[Cj]

    return sim_Ci_Cj
