import spacy
import pathlib
import docx
nlp = spacy.load('ja_ginza')

p = pathlib.Path(r"C:\Users\nutta\OneDrive\ドキュメント\授業資料")
file_list = list(p.glob("*.docx"))

doclist = []
for n in range(5):
  print(file_list[n])
  txt = ""
  doc = docx.Document(file_list[n])
  for par in doc.paragraphs:
    txt += par.text
  doclist.append(txt)
  n += 1


# doc1 = nlp('猫はこの世で一番可愛い生き物なので猫と一緒に眠ると幸せになれる')
# doc2 = nlp('ホットケーキに挟まれて眠りたい')
# doc3 = nlp('台湾カステラを敷き布団にして眠りたい')

for line in doclist:
  print(nlp(doclist[0]).similarity(nlp(line)))


# print(doc1.similarity(doc2))
# print(doc1.similarity(doc3))
# print(doc2.similarity(doc3))