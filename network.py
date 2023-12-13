import nlplot
import pandas as pd
import matplotlib as plt
from wc import database
from plotly.offline import iplot

text_list = []

result = database.get_allfiles()

for file in result:
    text_list.append(file.cutwords)

df = pd.DataFrame({"text": text_list})

npt = nlplot.NLPlot(df, target_col="text")

with open("wc\stopword.txt", "r", encoding="utf-8") as f:
    stopwords = [line.strip() for line in f.readlines()]

npt.build_graph(stopwords=stopwords, min_edge_frequency=0)
fig_co_network = npt.co_network(
    title="共起ネットワーク",
    # top_n=30,
    width=800,
    height=800,
    # fig_save_path="co_network.png",
)
iplot(fig_co_network)
