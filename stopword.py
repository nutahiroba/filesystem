from nltk.corpus import stopwords
import nltk

# wgetメソッドでhttp://svn.sourceforge.jp/svnroot/slothlib/CSharp/Version1/SlothLib/NLP/Filter/StopWord/word/Japanese.txtを持ってくる
# （windwsの場合
# wget http://svn.sourceforge.jp/svnroot/slothlib/CSharp/Version1/SlothLib/NLP/Filter/StopWord/word/Japanese.txt -OutFile Japanese.txt
# を実行）

stoppath = "Japanese.txt"
with open(stoppath, "r", encoding= "utf-8") as f:
  stop_words = f.readlines()

# # nltkモジュールから取得したstopwords
# with open("English.txt", "r", encoding="utf-8") as f:
#   en_stopwords = f.readlines()

# en_sw = en_stopwords[0].replace(",|[|]| ", "")
# for word in en_sw.split(","):
#   stopwords.append(word[2:-1])

nltk.download('stopwords')
en_stop_words = stopwords.words('english')

for word in en_stop_words:
  stop_words.append(word)

stop_words = [string.strip() for string in stop_words if string.strip()]

with open("stopword.txt", "w", encoding= "utf-8") as f:
  for word in stop_words:
    print(word, file = f)