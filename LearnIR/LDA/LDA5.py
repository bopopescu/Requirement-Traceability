from gensim import corpora, models, similarities

dictionary = corpora.Dictionary.load('../../tmp/deerwester.dict')
corpus = corpora.MmCorpus('../..//tmp/deerwester.mm')
print(corpus)

lsi = models.LsiModel(corpus, id2word=dictionary, num_topics=2)
doc = "human computer interaction"
vec_bow = dictionary.doc2bow(doc.lower().split())
vec_lsi = lsi[vec_bow]  # convert the query to LSI space
print(vec_lsi)

# transform corpus to space and index it
index = similarities.MatrixSimilarity(lsi[corpus])

index.save('/tmp/deerwester.index')
sims = index[vec_lsi]
sims = sorted(enumerate(sims), key=lambda item: -item[1])

from pprint import pprint

pprint(sims)