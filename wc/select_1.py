# 使わなかった機能が入ってる

import pathlib
import datetime
import os
import glob
import re
import MeCab
import docx
import csv
import pandas as pd

# ---------------------------ファイル名取得--------------------------

# パスの指定
p = pathlib.Path(r"C:\Users\nutta\OneDrive\ドキュメント\授業資料")
file_list = list(p.glob("*.docx"))


# 日本語が入るとglobが対応できない？ not listと出る
# file = glob.glob(r"C:\Users\nutta\OneDrive\ドキュメント\授業資料\*.docx")
# print(os.path.split(file))


dataset = [0] * (len(file_list) + 1)
dataset[0] = ["ファイル名", "作成日時", "最終更新日時", "ファイルサイズ(Byte)", "再頻出語(上位3件)", "冒頭"]
n = 1

wordtype = "名詞" or "形容詞"
# ファイル名の出力
for line in file_list:
    # print(line.name)

    # ----------------------タイムスタンプの取得--------------------------

    # pathlib.Path.statでもos.statでもos.stat_resultオブジェクトを取得できる
    st = pathlib.Path.stat(line)
    # print(st.st_atime)

    # 取得したUNIX時間を日時に変換
    # - atime: 最終アクセス日時
    # - mtime: 最終内容更新日時
    # - ctime: メタデータの最終更新日時（UNIX） / 作成日時（Windows）
    a_dt = datetime.datetime.fromtimestamp(st.st_atime)
    access_time = a_dt.strftime("%Y年%m月%d日 %H:%M:%S")
    m_dt = datetime.datetime.fromtimestamp(st.st_mtime)
    make_time = m_dt.strftime("%Y年%m月%d日 %H:%M:%S")

    # 数字のみ
    # print("最終更新日時：{}".format(dt))

    # print(dt.strftime('%Y年%m月%d日 %H:%M:%S'))

    # -----------------ファイルサイズ取得----------------------------
    date_size = os.path.getsize(line)

    # --------------------最頻語上位5位--------------------------------
    tagger = MeCab.Tagger()
    doc = docx.Document(line)

    txt = ""

    for par in doc.paragraphs:
        txt += par.text

    # tagger.parse(txt).split()

    mecabTagger = MeCab.Tagger()
    noun_count = {}

    node = mecabTagger.parseToNode(txt)
    while node:
        word = node.surface
        hinshi = node.feature.split(",")[0]
        if word in noun_count.keys() and hinshi == wordtype:
            noun_freq = noun_count[word]
            noun_count[word] = noun_freq + 1
        elif hinshi == wordtype:
            noun_count[word] = 1
        else:
            pass
        node = node.next

    noun_count = sorted(noun_count.items(), key=lambda x: x[1], reverse=True)

    # -------------------データセットに保存-----------------------------
    dataset[n] = [
        line.name,
        make_time,
        access_time,
        date_size,
        noun_count[:3],
        txt[:20],
    ]
    n += 1

for line in dataset:
    print(line)


# # -------------------------CSVファイルで出力--------------------------

# csv_path = r"C:\Users\nutta\myProject\FileSystem\test.txt"

# with open(csv_path, 'w', newline='') as file:
#     writer = csv.writer(file)
#     writer.writerow(dataset)
