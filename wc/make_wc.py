# 辞書orテキストからwcをsvgで作成
from wordcloud import WordCloud


def get(words, para):
    # print(para.color, para.width, para.height, para.step, para.min, para.max)
    wc = WordCloud(
        font_path="yumin.ttf",
        prefer_horizontal=1,
        background_color="white",
        # ~~~~~ここまでデフォルト~~~~~
        # grayでモノクロ、jetでRGB
        colormap=para.color,
        width=para.width,
        height=para.height,
        font_step=para.step,
        min_font_size=para.min,
        max_font_size=para.max,
    )

    metric = para.metric

    # if metric == "tf":
    #     dict =
    if type(words) == dict:
        wc.generate_from_frequencies(words)
    elif type(words) == str:
        wc.generate_from_text(words)
    else:
        print("This is unravaliable")
        return None

    return wc
