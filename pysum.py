# 参考：https://resanaplaza.com/2022/05/19/%E3%80%90%E5%AE%9F%E8%B7%B5%E3%80%91python%EF%BC%8Bpysummarization%E3%81%A7%E6%96%87%E6%9B%B8%E8%A6%81%E7%B4%84%EF%BC%88%E3%83%86%E3%82%AD%E3%82%B9%E3%83%88%E3%83%9E%E3%82%A4%E3%83%8B%E3%83%B3/

from pysummarization.nlpbase.auto_abstractor import AutoAbstractor
from pysummarization.tokenizabledoc.mecab_tokenizer import MeCabTokenizer
from pysummarization.abstractabledoc.top_n_rank_abstractor import TopNRankAbstractor

def document_summarize(file):
  # ファイル読み込み
  with open(file, encoding = "utf-8") as f:
    contents = f.readlines()
  
  # 行の結合
  document = "".join(contents)
  # 自動要約のオブジェクト生成
  auto_abstractor = AutoAbstractor()
  # トークナイザーにMeCabを選択
  auto_abstractor.tokenizable_doc = MeCabTokenizer()
  # 文書の区切り文字を選択
  auto_abstractor.delimiter_list = ["。", "\n"]
  # ドキュメントの抽象化を行うオブジェクトを生成
  abstractable_doc = TopNRankAbstractor()
  # 文書の要約を実行
  result_dict = auto_abstractor.summarize(document, abstractable_doc)

  return [x.replace("\n", ",") for x in result_dict["summarize_result"]]

# document  = "スタートレックには長い歴史がある。現在も人気が衰えず、次々と新作が登場している。"
# auto_abstractor = AutoAbstractor()
# auto_abstractor.tokenizable_doc = MeCabTokenizer()
# auto_abstractor.delimiter_list = ["。", "\n"]
# abstractable_doc = TopNRankAbstractor()
# result_dict = auto_abstractor.summarize(document, abstractable_doc)

# for line in result_dict["summarize_result"]:
#   print(line)

lines = document_summarize(r"C:\Users\nutta\myProject\FileSystem\sample1.txt")

for line in lines:
  print(line)