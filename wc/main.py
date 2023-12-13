# メインのプログラムコード
import os
import docx
import json
import pathlib
import datetime

from wc import make_wc, database


class Parameter:
    def __init__(self, color, width, height, min):
        self.color = color
        self.width = width
        self.height = height
        self.min = min


def get_ts(filepass):
    st = pathlib.Path.stat(filepass)
    # 最終アクセス時間
    # a_dt = datetime.datetime.fromtimestamp(st.st_atime)
    # strftimeで日付、時刻→ストリング
    # access_t = a_dt.strftime('%Y年%m月%d日 %H:%M:%S')
    # 最終更新時間
    # ローカルな時間を返す
    m_dt = datetime.datetime.fromtimestamp(st.st_mtime)
    make_t = m_dt.strftime("%Y年%m月%d日 %H:%M:%S")
    # c_dt = datetime.datetime.fromtimestamp(st.st_ctime)
    # create_t = m_dt.strftime('%Y年%m月%d日 %H:%M:%S')

    return make_t


def PathtoMeta(path):
    doc = docx.Document(path)  # ファイル名を実際のファイル名に置き換える
    title = str(path).split("\\")[-1]

    # メタデータを取得
    metadata = {
        "Title": title,
        # 'Title': doc.core_properties.title,
        # 'Author': doc.core_properties.author,
        # 'Subject': doc.core_properties.subject,
        # 'Keywords': doc.core_properties.keywords,
        # 'Comments': doc.core_properties.comments,
        # 'Last Modified By': doc.core_properties.last_modified_by,
        "Revision": doc.core_properties.revision,
        "Created": doc.core_properties.created,
        "Modified": doc.core_properties.modified,
        "file_size": os.path.getsize(path),
        "os_mtime": get_ts(path),
    }
    return metadata


def set_to_list(obj):
    if isinstance(obj, set):
        return list(obj)
    return obj


def convert_to_json_serializable(obj, memo=None):
    if memo is None:
        memo = set()

    if id(obj) in memo:
        # 循環参照の場合は None を返す
        return None

    memo.add(id(obj))

    if isinstance(obj, set):
        return list(obj)
    elif isinstance(obj, dict):
        return {
            key: convert_to_json_serializable(value, memo) for key, value in obj.items()
        }
    elif isinstance(obj, list):
        return [convert_to_json_serializable(element, memo) for element in obj]
    return obj


def makeDB(path):
    folder_path = pathlib.Path(path)
    # フォルダの指定
    file_list = folder_path.glob("*.docx")

    # wordshash = []
    cutwordslist = []
    # try:
    #     with open("tfdict.json", "r", encoding="utf-8") as f:
    #         all_tfdict = json.load(f)
    # except FileNotFoundError:
    #     all_tfdict = {}

    # try:
    #     with open("dfdict.json", "r", encoding="utf-8") as f:
    #         all_dfdict = json.load(f)
    # except FileNotFoundError:
    #     all_dfdict = {}

    # for path in file_list:
    #     # メタデータを取得
    #     metadata = PathtoMeta(path)

    #     # 内容をDBに保存
    #     dbval = database.makeDB(path)

    #     if dbval is None:
    #         continue
    #     else:
    #         tfdict, cutwords, words_infile = dbval
    #         # フォルダ全体の単語リスト
    #         for tf in tfdict:
    #             if tf in all_tfdict:
    #                 all_tfdict[tf] += tfdict[tf]
    #             else:
    #                 all_tfdict[tf] = tfdict[tf]

    #         for word in words_infile:
    #             if word in dfdict:
    #                 dfdict[word] += words_infile[word]
    #             else:
    #                 dfdict[word] = words_infile[word]

    #         # 単語リスト
    #         cutwordslist.append(" ".join(cutwords))

    #         # json_string = json.dumps(all_tfdict, default=convert_to_json_serializable)

    all_dfdict, all_tfdict = database.regDB(file_list)

    with open("tfdict.json", "w", encoding="utf-8") as f:
        json.dump(all_tfdict, f, ensure_ascii=False)

    with open("dfdict.json", "w", encoding="utf-8") as f:
        json.dump(all_dfdict, f, ensure_ascii=False)

    return cutwordslist

    # 動かんからパス
    # tfitfdict = tfidf.getvalues(cutwordslist)


def makeWC(para):
    try:
        with open("tfdict.json", "r", encoding="utf-8") as f:
            all_tfdict = json.load(f)
    except FileNotFoundError:
        all_tfdict = {}

    try:
        with open("dfdict.json", "r", encoding="utf-8") as f:
            dfdict = json.load(f)
    except:
        dfdict = {}

    # wc = make_wc.get(dfdict, para)

    numeral = para.numeral
    commonNoun = para.commonNoun
    properNoun = para.properNoun

    # print(numeral[0], numeral[0] is True)
    # print(commonNoun[0], commonNoun[0] is None)
    # print(properNoun, properNoun is True)

    with open("word_index.json", "r", encoding="utf-8") as f:
        words_index = json.load(f)
    words = ""
    if numeral[0]:
        numeral_text = " ".join(words_index["数詞"])
        words += numeral_text
    if commonNoun[0]:
        commonNoun_text = " ".join(words_index["普通名詞"])
        words += commonNoun_text
    if properNoun:
        proper_text = " ".join(words_index["固有名詞"])
        words += proper_text

    wc = make_wc.get(words, para)

    # wc = make_wc.get(all_tfdict, para)

    return wc.to_svg()

    # file_path = "templates\wc3.html"
    # wc2html.get(wc, file_path)


def row_to_dict(row):
    return ", ".join([f"{column}: {value}" for column, value in row.items()])


def check(words):
    row_files = database.getval(words)
    result_files = {}
    for file in row_files:
        tmp = str(file.path)
        words_val = [file.cutwords, file.tfdict]
        result_files[tmp] = file.cutwords.replace("'", "").replace(" ", "")[1:-1]
    return result_files


def getfiles(received_words, match_files):
    with open("tfidfdict.json", "r", encoding="utf-8") as f:
        tfidfdict = json.load(f)
    result_files = {}
    for file in match_files:
        tmp = {}
        for word in received_words:
            tmp[word] = tfidfdict[word][file]
            result_files[file] = tmp
    return result_files


p = pathlib.Path(r"C:\Users\nutta\OneDrive\ドキュメント\授業資料")
makeDB(p)

# para = Parameter(color="jet", width=600, height=600, min=15)
# wc = makeWC(p)

# print(wc)
