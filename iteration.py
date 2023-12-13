# https://zenn.dev/robes/articles/a3e1a6e80efd99#%E5%85%B1%E8%B5%B7%E8%A1%8C%E5%88%97%E3%81%AE%E4%BD%9C%E6%88%90

import itertools
from wc import database
import collections
import pandas as pd
import re

pattern = re.compile(r"^(?:\d+|[A-Za-z]+)$")

# 文書ごとの単語リストを作成
result = database.get_allfiles()
sentences = []
# 一つのリストにする
target_combs = []
for file in result[:50]:
    sentence = []
    for word in file.cutwords[1:-1].split(","):
        if len(word) != 1 and pattern.match(word) is None:
            sentence.append(word)
    sentences.append(sentence)

    # 文章から可能な限りの単語の組を作成
    sentences_combs = [list(itertools.combinations(sentence, 2))]

    # 重複を消すためにタプルに変更、リストをソート
    words_combs = [
        [tuple(sorted(words)) for words in sentence] for sentence in sentences_combs
    ]
    for words_comb in words_combs[0]:
        tuple1, tuple2 = words_comb[0], words_comb[1]
        if (
            tuple1
            != tuple2
            #     and len(tuple1) != 1
            #     and len(tuple2) != 1
            #     and pattern.match(tuple1) is None
            #     and pattern.match(tuple2) is None
        ):
            target_combs.append(words_comb)

    # words_combs = [
    #     [tuple(sorted(words)) for words in sentence] for sentence in sentences_combs
    # ]
    # for words_comb in words_combs:
    #     target_combs.extend(words_comb)
    ct = collections.Counter(target_combs)

    df = pd.DataFrame(
        [{"1番目": i[0][0], "2番目": i[0][1], "count": i[1]} for i in ct.most_common()]
    )

print(df)


def kyoki_network(df):
    from pyvis.network import Network

    got_net = Network(
        height="1000px",
        width="95%",
        bgcolor="#FFFFFF",
        font_color="black",
        notebook=True,
    )

    got_net.force_atlas_2based()
    got_data = df[:150]

    sources = got_data["1番目"]  # count
    targets = got_data["2番目"]  # first
    weights = got_data["count"]  # second

    edge_data = zip(sources, targets, weights)

    for e in edge_data:
        src = e[0]
        dst = e[1]
        w = e[2]

        got_net.add_node(src, src, title=src)
        got_net.add_node(dst, dst, title=dst)
        got_net.add_edge(src, dst, value=w)

    neighbor_map = got_net.get_adj_list()

    for node in got_net.nodes:
        node["title"] += " Neighbors:<br>" + "<br>".join(neighbor_map[node["id"]])
        node["value"] = len(neighbor_map[node["id"]])

    got_net.show_buttons(filter_=["physics"])
    return got_net


got_net = kyoki_network(df)
got_net.show("kyoki.html")
