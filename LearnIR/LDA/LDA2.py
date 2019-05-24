import numpy as np
import lda
import lda.datasets
'''
LDA库
'''
# # document-term matrix
X = lda.datasets.load_reuters()
# print("type(X): {}".format(type(X)))
# print("shape: {}\n".format(X.shape))
# print(X[:5, :5])        #前五行的前五列
#
# # the vocab
vocab = lda.datasets.load_reuters_vocab()
# print("type(vocab): {}".format(type(vocab)))
# print("len(vocab): {}\n".format(len(vocab)))
# print(vocab[:5])
#
# # titles for each story
titles = lda.datasets.load_reuters_titles()
# print("type(titles): {}".format(type(titles)))
# print("len(titles): {}\n".format(len(titles)))
# print(titles[:5])       # 打印前五个文档的标题
#
# print("\n************************************************************")
# doc_id = 0
# word_id = 0
# while doc_id < 5:
#     print("doc id: {} word id: {}".format(doc_id, word_id))
#     print("-- count: {}".format(X[doc_id, word_id]))
#     print("-- word : {}".format(vocab[word_id]))
#     print("-- doc  : {}\n".format(titles[doc_id]))
#     doc_id += 1
#
topicCnt = 20
model = lda.LDA(n_topics = topicCnt, n_iter = 500, random_state = 1)
model.fit(X)          # model.fit_transform(X) is also available

# print("\n************************************************************")
topic_word = model.topic_word_
# print("type(topic_word): {}".format(type(topic_word)))
# print("shape: {}".format(topic_word.shape))
# print(vocab[:3])
# print(topic_word[:, :3])    #打印所有行(20)行的前3列
#
# for n in range(20):
#     sum_pr = sum(topic_word[n,:])   # 第n行所有列的比重之和，等于1
#     print("topic: {} sum: {}".format(n, sum_pr))
#
# print("\n************************************************************")
# n = 5
# for i, topic_dist in enumerate(topic_word):
#     topic_words = np.array(vocab)[np.argsort(topic_dist)][:-(n+1):-1]
#     print('*Topic {}\n- {}'.format(i, ' '.join(topic_words)))
#
# print("\n************************************************************")
doc_topic = model.doc_topic_
# print("type(doc_topic): {}".format(type(doc_topic)))
# print("shape: {}".format(doc_topic.shape))
# for n in range(10):
#     topic_most_pr = doc_topic[n].argmax()
#     print("doc: {} topic: {}".format(n, topic_most_pr))
#
# print("\n************************************************************")
import matplotlib.pyplot as plt

# f, ax = plt.subplots(5, 1, figsize=(8, 6), sharex=True)
# for i, k in enumerate([0, 5, 9, 14, 19]):
#     print(i, k)
#     ax[i].stem(topic_word[k, :], linefmt='b-',
#                markerfmt='bo', basefmt='w-')
#     ax[i].set_xlim(-50, 4350)
#     ax[i].set_ylim(0, 0.08)
#     ax[i].set_ylabel("Prob")
#     ax[i].set_title("topic {}".format(k))
#
# ax[4].set_xlabel("word")
#
# plt.tight_layout()
# plt.show()
#
# print("\n************************************************************")
f, ax = plt.subplots(5, 1, figsize=(8, 6), sharex=True)
for i, k in enumerate([1, 3, 4, 8, 9]):
    ax[i].stem(doc_topic[k, :], linefmt='r-',
               markerfmt='ro', basefmt='w-')
    ax[i].set_xlim(-1, 21)
    ax[i].set_ylim(0, 1)
    ax[i].set_ylabel("Prob")
    ax[i].set_title("Document {}".format(k))

ax[4].set_xlabel("Topic")

plt.tight_layout()
plt.show()

