# 文字列の単語数をカウントして辞書とリストを返す
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
import MeCab
import random
import string
from pprint import pprint
import docx
import hashlib
import re
import json

# from wc import title_model

engine = create_engine("sqlite:///words.db", echo=False)
Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()

pattern = re.compile(r"^\d+$")

class Files(Base):
    __tablename__ = "files"
    id = Column(String, primary_key=True)
    path = Column(String, unique=True)
    # title = Column(String)
    cutwords = Column(String, unique=True)
    tfdict = Column(String)

    def __init__(self, id, path, cutwords, tfdict):
        self.id = id
        self.path = path
        # self.title = title
        self.cutwords = cutwords
        self.tfdict = tfdict

    def __str__(self):
        return f"id:{self.id},path:{self.path},cutwords:{self.cutwords},tfdict:{self.tfdict}"
        # return f"id:{self.id},path:{self.path},title:{self.title},cutwords:{self.cutwords},tfdict:{self.tfdict}"


Base.metadata.create_all(engine)


def PathtoTxt(path):
    if ".docx" in str(path):
        doc = docx.Document(path)
        words = ""
        for par in doc.paragraphs:
            words += par.text.replace("\u2028", "")
    elif ".txt" in str(path):
        # 行ごとに分割
        with open(path, encoding="utf-8") as f:
            contents = f.readlines()
        words = "".join(contents)
    return words


def converttostr(input_list):
    return " ".join(map(str, input_list))


def converttolist(input_str):
    return input_str.split()


# 指定されたパスのドキュメントがすでに存在するかをチェックする関数
def ispath_exists(path):
    path = str(path)
    exists = session.query(Files).filter(Files.path == path).count()
    if exists != 0:
        return True
    # ループがすべてのファイルを検査し終えても一致するものが見つからない場合
    return False


def dbgetfile(path):
    path = str(path)
    file = session.query(Files).filter(Files.path == path).first()
    if file is not None:
        return file.cutwords, file.tfdict
    else:
        print("404 指定されたパスのドキュメントが見つかりませんでした")
        return None


def genid(length=8):
    characters = string.ascii_letters + string.digits
    random_id = "".join(random.choice(characters) for _ in range(length))
    return random_id


def regtodb(path, cutwords, tfdict):
    path_str = str(path)
    # 辞書オブジェクトを文字列に変換
    tfdict_str = str(tfdict).replace(" ", "").replace("'", "")
    cutwords_str = str(cutwords).replace(" ", "").replace("'", "")
    # title_str = str(title).replace(" ", "").replace("'", "")
    id = genid()
    # DBに登録
    file = Files(
        id=id,
        path=path_str,
        # title=title_str,
        cutwords=cutwords_str,
        tfdict=tfdict_str,
    )
    session.add(file)
    session.commit()


def getval(words):
    result = (
        session.query(Files)
        .filter(*[Files.cutwords.contains(word) for word in words])
        .all()
    )
    return result


def get_allfiles():
    result = session.query(Files).all()
    return result


def is_new(cutwords):
    if (
        session.query(Files)
        .filter(Files.cutwords == str(cutwords).replace(" ", "").replace("'", ""))
        .count()
        == 0
    ):
        return True
    else:
        return False


def words_split(words):
    tagger = MeCab.Tagger()
    node = tagger.parseToNode(words)
    # print("version:",tagger.version())  # MeCabのバージョン情報
    # print("dic",tagger.dictionary_info().filename)
    # while node:
    # print(node.surface, node.cost)
    #     node = node.next
    return node


def read_files(path):
    with open(path, "r", encoding="utf-8") as f:
        stopwords = f.readlines()
    stopwords = [string.strip() for string in stopwords if string.strip()]
    return stopwords


def wordtolist(path, word_index):
    # dbfile = dbgetfile(path)
    if ispath_exists(path):
        return None, word_index
    # 文字列取得
    words = PathtoTxt(path)

    stopwords = read_files(r"C:\Users\nutta\myProject\FileSystem\wc\stopword.txt")

    if words == "":
        return None, word_index
    cutwords = []

    tagger = MeCab.Tagger()
    node = tagger.parseToNode(words)

    word_type = "名詞"

    while node:
        word = node.surface
        hinshi = node.feature.split(",")[0]
        sub_hinshi = node.feature.split(",")[1]

        if hinshi == word_type and word not in stopwords and len(word) != 1:
            cutwords.append(word)
            if sub_hinshi in word_index:
                word_index[sub_hinshi].append(word)
            else:
                word_index[sub_hinshi] = [word]

        node = node.next
    # tfdict = sorted(tfdict.items(), key = lambda x:x[1], reverse=True)
    # if is_new(cutwords):
    #     regtodb(path, cutwords, tfdict)
    # else:
    #     return None
    return cutwords, word_index


def regDB(files):
    all_tfdict = {}
    all_dfdict = {}
    word_index = {}
    for file in files:
        cutwords, word_index = wordtolist(file, word_index)
        if cutwords is None:
            continue
        else:
            tfdict = {}
            dflist = []
            for word in cutwords:
                if word not in dflist:
                    dflist.append(word)
                    tfdict[word] = cutwords.count(word)

            if is_new(cutwords):
                regtodb(file, cutwords, tfdict)
            else:
                pass

            for word in dflist:
                if word in all_dfdict.keys():
                    all_tfdict[word] += tfdict[word]
                    all_dfdict[word] += 1
                else:
                    all_tfdict[word] = tfdict[word]
                    all_dfdict[word] = 1

    with open("word_index.json", "w", encoding="utf-8") as f:
        json.dump(word_index, f, ensure_ascii=False)

    return all_dfdict, all_tfdict


def pre_makedb(path):
    # dbfile = dbgetfile(path)
    if ispath_exists(path):
        return None

    with open(
        r"C:\Users\nutta\myProject\FileSystem\wc\stopword.txt", "r", encoding="utf-8"
    ) as f:
        stopwords = f.readlines()
    stopwords = [string.strip() for string in stopwords if string.strip()]

    # 文字列取得
    words = PathtoTxt(path)
    # title = title_model.get_title(words)
    if words == "":
        return None
    cutwords = []
    tfdict = {}
    words_infile = {}

    tagger = MeCab.Tagger()
    node = tagger.parseToNode(words)

    # node = words_split(words)
    while node:
        word = node.surface
        hinshi = node.feature.split(",")[0]
        if hinshi == "名詞" and word not in stopwords:
            cutwords.append(word)
        # dfではなく、ファイルの単語の有無を確認している
        if word in tfdict.keys():
            tfdict[word] += 1
            pass
        elif (
            hinshi == "名詞"
            and len(word) != 1
            and word not in stopwords
            and pattern.match(word) is None
        ):
            tfdict[word] = 1
            words_infile[word] = 1
        else:
            pass
        node = node.next
    # tfdict = sorted(tfdict.items(), key = lambda x:x[1], reverse=True)
    if is_new(cutwords):
        regtodb(path, cutwords, tfdict)
    else:
        return None
    return tfdict, cutwords, words_infile


# node = words_split("彼女はペンパイナッポーアッポーペンと恋ダンスを踊った。")

# DBに依存しないタイプ
# def raw_getcount(words):
#     tagger = MeCab.Tagger()
#     cutwords = []

#     with open(
#         r"C:\Users\nutta\myProject\FileSystem\wc\stopword.txt", "r", encoding="utf-8"
#     ) as f:
#         stopwords = f.readlines()
#     stopwords = [string.strip() for string in stopwords if string.strip()]

#     tfdict = {}
#     node = tagger.parseToNode(words)
#     while node:
#         word = node.surface
#         hinshi = node.feature.split(",")[0]
#         if hinshi == "名詞" and word not in stopwords:
#             cutwords.append(word)

#         if hinshi == "名詞" and word in tfdict.keys():
#             # tfdict[word] += 1
#             pass
#         elif hinshi == "名詞" and len(word) != 1 and word not in stopwords:
#             tfdict[word] = 1
#         else:
#             pass
#         node = node.next
#     # tfdict = sorted(tfdict.items(), key = lambda x:x[1], reverse=True)
#     return tfdict, cutwords
