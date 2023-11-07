# 文字列の単語数をカウントして辞書とリストを返す

import MeCab

def getcount(words):
  tagger = MeCab.Tagger()
  cutwords = []

  with open("stopword.txt", "r",encoding="utf-8") as f:
    stopwords = f.readlines()
  stopwords = [string.strip() for string in stopwords if string.strip()]

  noundict = {}
  node = tagger.parseToNode(words)
  while node:
    word = node.surface
    hinshi = node.feature.split(",")[0]
    cutwords.append(word)

    if hinshi == "名詞" and word in noundict.keys():
      noundict[word] += 1
    elif hinshi == "名詞" and len(word) != 1 and word not in stopwords:
      noundict[word] = 1
    else:
      pass
    node = node.next
  # noundict = sorted(noundict.items(), key = lambda x:x[1], reverse=True)
  return noundict, cutwords
