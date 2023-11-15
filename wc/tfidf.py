# 文字列からtfidf値の計算

import MeCab
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd


def wakachi(text):
    mecab = MeCab.tagger()
    return mecab.parse(text).strip().split("")


def getvalues(cutwordslist):
    tfidfdict = {}
    vecs = TfidfVectorizer(
        # tokenizer= wakachi, smooth_idf=False
    )
    X = vecs.fit_transform(cutwordslist)
    words = vecs.get_feature_names_out()
    # print('feature_names:', words)
    for doc_id, vec in zip(range(len(cutwordslist)), X.toarray()):
        # print('doc_id:', doc_id + 1)
        tmplist = []
        newlist = sorted(enumerate(vec), key=lambda x: x[1], reverse=True)
        for n in range(5):
            tmplist.append(words[newlist[n][0]])
        # for w_id, tfidf in sorted(enumerate(vec), key=lambda x: x[1], reverse=True):
        #     lemma = words[w_id]
        #     print(w_id, tfidf)
        #     if tfidf != 0:
        #       print('\t{0:s}: {1:f}'.format(lemma, tfidf))
        #     if w_id < 10:
        #         tmplist.append(lemma)
        tfidfdict[doc_id + 1] = tmplist

    return tfidfdict


# tdidvectorizerを使用しないバージョン
import database
import json


# tf値を算出
def str_to_tfdict(file):
    tfs = file.tfdict[1:-1].split(",")
    doc = {}
    for tf in tfs:
        word, count = tf.split(":")
        count = int(count)
        doc[word] = count
    tmp = {}
    for word in doc.keys():
        tmp[word] = doc[word] / sum(doc.values())
    doc = tmp
    return doc


def calc_tfidf():
    files = database.get_allfiles()
    tfs = {}
    for file in files:
        tfs[file.path] = str_to_tfdict(file)
    with open("dfdict.json", "r", encoding="utf-8") as f:
        dfdict = json.load(f)
        idf = {}
        for word in dfdict.keys():
            idf[word] = np.log((len(files) / dfdict[word]) + 1)
    return tfs, idf


calc_tfidf()
