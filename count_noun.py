import MeCab

def getcount(words):
  tagger = MeCab.Tagger()
  cutwords = []

  noundict = {}
  node = tagger.parseToNode(words)
  while node:
    word = node.surface
    hinshi = node.feature.split(",")[0]
    if hinshi == "名詞":
      cutwords.append(word)
    if hinshi == "名詞" and word in noundict.keys():
      noundict[word] += 1
    elif hinshi == "名詞":
      noundict[word] = 1
    else:
      pass
    node = node.next
  noundict = sorted(noundict.items(), key = lambda x:x[1], reverse=True)
  return noundict, cutwords
