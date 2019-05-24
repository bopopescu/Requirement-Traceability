
from gensim import corpora, models, similarities

def useTFIDFModel(sourceArtifact, dictionary, corpus):
    # set tfidf model
    tfidf = models.TfidfModel(corpus)
    featureNum = len(dictionary.token2id.keys())
    # index = similarities.SparseMatrixSimilarity(tfidf[corpus], num_features=featureNum)
    index = similarities.MatrixSimilarity(tfidf[corpus])

    # 源文件(UseCase)
    # UseCase为UTF-8编码
    fo = open(sourceArtifact, "r", encoding="UTF-8")
    new_doc = fo.read()
    # the word 'interaction' does not appear in the dictionary and is ignored
    new_doc_array = new_doc.lower().split()
    # print("new_doc.lower().split()     " + str(new_doc_array))

    # 文本预处理
    import TextPreprocess
    new_doc_vec = TextPreprocess.textProprocessOneFile(document=new_doc_array)

    # print("TextPreprocess.textProprocessOneFile     " + str(new_doc_vec))
    new_vec = dictionary.doc2bow(new_doc_vec)
    # print(new_vec)
    ml_tfidf = tfidf[new_vec]

    sims = index[ml_tfidf]

    return sims

def getCodeTextSim(Ci, Cj, dictionary, corpus):
    # corpus_Ci = corpus[Ci]
    # set tfidf model
    tfidf = models.TfidfModel(corpus)
    featureNum = len(dictionary.token2id.keys())
    # index = similarities.SparseMatrixSimilarity(tfidf[corpus], num_features=featureNum)
    index = similarities.MatrixSimilarity(tfidf[corpus])

    # print("corpus[Ci]=", corpus[Ci])
    # index = similarities.MatrixSimilarity()
    # index = similarities.SparseMatrixSimilarity(tfidf[corpus_Ci], num_features=featureNum)

    Ci_vector = corpus[Ci]
    ml_tfidf = tfidf[Ci_vector]

    sims = index[ml_tfidf]
    # print("Ci sims=", sims)
    sim_Ci_Cj = sims[Cj]

    return sim_Ci_Cj
