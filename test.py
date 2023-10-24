import pass2txt
import count_noun
from nltk.corpus import stopwords
import nltk


with open("stopword.txt", "r",encoding="utf-8") as f:
  stopwords = f.readlines()

stopwords = [string.strip() for string in stopwords if string.strip()]

for word in stopwords:
  print(word)

# nltk.download('stopwords')
# stop_words = stopwords.words('english')
# print(stop_words)

# stoppath = "Japanese.txt"
# with open(stoppath, "r", encoding= "utf-8") as f:
#   stopwords = f.readlines()

# # nltkモジュールから取得したstopwords
# with open("English.txt", "r", encoding="utf-8") as f:
#   en_stopwords = f.readlines()

# en_sw = en_stopwords[0].replace(",|[|]| ", "")
# for word in en_sw.split(","):
#   stopwords.append(word[2:-1])

# stopwords = [string.strip() for string in stopwords if string.strip()]

# print(stopwords)

# p = r"C:\Users\nutta\OneDrive\ドキュメント\授業資料\(学類長・専門学群長宛)平成31年度座長団選出報告書.docx"

# p2 = r"C:\Users\nutta\myProject\FileSystem\sample1.txt"

# words = pass2txt.getwords(p2)

# print(count_noun.getcount(words))


# stoppath = "Japanese.txt"
# with open(stoppath, "r", encoding = "utf-8") as f:
#   stopwords = f.readlines()

# stopwords = [string.strip() for string in stopwords if string.strip()]
# print(stopwords[:3])