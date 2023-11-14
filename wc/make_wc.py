# 辞書orテキストからwcをsvgで作成
from wordcloud import WordCloud


def get(words, para):
    wc = WordCloud(
        font_path="C:\Windows\Fonts\yumin.ttf",
        prefer_horizontal=1,
        background_color="white",
        # ~~~~~ここまでデフォルト~~~~~
        # grayでモノクロ、jetでRGB
        colormap=para.color,
        width=para.width,
        height=para.height,
        # font_stepが動作しない
        font_step=7,
        min_font_size=para.min,
    )

    if type(words) == dict:
        wc.generate_from_frequencies(words)
    elif type(words) == str:
        wc.generate_from_text(words)
    else:
        print("This is unravaliable")
        return None

    return wc
