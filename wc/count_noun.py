# 文字列の単語数をカウントして辞書とリストを返す
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import MeCab
import random
import string
from pprint import pprint

engine = create_engine('sqlite:///words.db', echo=True)
Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()
class Files(Base):
  __tablename__ = "files"
  id = Column(String, primary_key=True)
  path = Column(String, unique=True)
  cutwords = Column(String)
  noundict = Column(String)

  def __init__(self,id, path, cutwords, noundict):
    self.id = id
    self.path = path
    self.cutwords = cutwords
    self.noundict = noundict

  def __str__(self):
    return f"id:{self.id},path:{self.path},cutwords:{self.cutwords},noundict:{self.noundict}"

Base.metadata.create_all(engine)

def converttostr(input_list):
  return ' '.join(map(str, input_list))

def converttolist(input_str):
  return input_str.split()

#指定されたパスのドキュメントがすでに存在するかをチェックする関数
def ispath_exists(path):
  path = str(path)
  exists = session.query(Files).filter(Files.path == path).count()
  # pprint(exists)
  # print(type(exists))
  if exists != 0:
    return True
  # ループがすべてのファイルを検査し終えても一致するものが見つからない場合
  return False

def dbgetfile(path):
  path = str(path)
  file = session.query(Files).filter(Files.path == path).first()
  # for file in files:
  if file is not None:
    return converttostr(file.cutwords), converttostr(file.noundict)
  else:
    # print("404 指定されたパスのドキュメントが見つかりませんでした")
    return None

def genid(length=8):
    characters = string.ascii_letters + string.digits
    random_id = ''.join(random.choice(characters) for _ in range(length))
    return random_id



def regtodb(path, cutwords, noundict):
    path_str = str(path)
    # 辞書オブジェクトを文字列に変換
    noundict_str = converttostr(noundict)
    cutwords_str = converttostr(cutwords)
    id = genid()
    #DBに登録
    file = Files(id=id, path=path_str, cutwords=cutwords_str, noundict=noundict_str)
    session.add(file)
    session.commit()

def getcount(path, words):
  # if ispath_exists(path):
  dbfile = dbgetfile(path)
  # print(dbfile)
  if dbfile is not None:
    return dbfile
  tagger = MeCab.Tagger()
  cutwords = []

  with open(r"C:\Users\nutta\myProject\FileSystem\wc\stopword.txt", "r",encoding="utf-8") as f:
    stopwords = f.readlines()
  stopwords = [string.strip() for string in stopwords if string.strip()]

  noundict = {}
  node = tagger.parseToNode(words)
  while node:
    word = node.surface
    hinshi = node.feature.split(",")[0]
    if hinshi == "名詞" and word not in stopwords:
      cutwords.append(word)

    if hinshi == "名詞" and word in noundict.keys():
      noundict[word] += 1
    elif hinshi == "名詞" and len(word) != 1 and word not in stopwords:
      noundict[word] = 1
    else:
      pass
    node = node.next
  # noundict = sorted(noundict.items(), key = lambda x:x[1], reverse=True)
  regtodb(path, noundict, cutwords)
  return noundict, cutwords

# DBに依存しないタイプ
def raw_getcount(words):
  tagger = MeCab.Tagger()
  cutwords = []

  with open(r"C:\Users\nutta\myProject\FileSystem\wc\stopword.txt", "r",encoding="utf-8") as f:
    stopwords = f.readlines()
  stopwords = [string.strip() for string in stopwords if string.strip()]

  noundict = {}
  node = tagger.parseToNode(words)
  while node:
    word = node.surface
    hinshi = node.feature.split(",")[0]
    if hinshi == "名詞" and word not in stopwords:
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
