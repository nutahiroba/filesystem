from wordcloud import WordCloud
import json


def make_wordcloud(dict, html_name):
    wc = WordCloud(
        font_path=r"C:\Users\nutta\myProject\FileSystem\YUMIN.TTF",
        prefer_horizontal=1,
        background_color="white",
        # ~~~~~ここまでデフォルト~~~~~
        # grayでモノクロ、jetでRGB
        colormap="Greys",
        width=600,
        height=600,
        font_step=20,
        min_font_size=20,
        max_font_size=200,
    )
    wc.generate_from_frequencies(dict)

    wc.to_file("wc.png")
    wordcloud = wc.to_svg()

    javascript = """

    <script>
    var textElements = document.getElementsByTagName("text");

    for (var i = 0; i < textElements.length; i++) {
        textElements[i].style.fill = "rgb(0, 0, 0)";
    }
    </script>

    """

    # html_name = r"../html_wc/" + html_name
    with open(html_name, "w", encoding="utf-8") as f:
        f.write(wordcloud)
        f.write(javascript)


def list_to_dict(word_list):
    word_count_dict = {}
    for word in word_list:
        if word in word_count_dict:
            word_count_dict[word] += 1
        else:
            word_count_dict[word] = 1
    return word_count_dict


def main():
    with open("word_index.json", "r", encoding="utf-8") as f:
        words_index = json.load(f)

    hinshis = ["数詞", "普通名詞", "固有名詞"]
    sub_hinshi = ["サ変可能", "一般", "副詞可能", "助数詞可能", "サ変形状詞可能", "形状詞可能"]

    for hinshi in ["数詞", "普通名詞", "固有名詞"]:
        if hinshi == "普通名詞":
            for sub_hinshi in ["サ変可能", "一般", "副詞可能", "助数詞可能", "サ変形状詞可能", "形状詞可能"]:
                make_wordcloud(
                    list_to_dict(words_index[hinshi][sub_hinshi]),
                    f"{hinshi}_{sub_hinshi}.html",
                )
        else:
            make_wordcloud(list_to_dict(words_index[hinshi]), f"{hinshi}.html")


main()
