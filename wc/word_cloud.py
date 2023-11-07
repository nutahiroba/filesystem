#ファイルパスからワードクラウドを作成するコード

from wordcloud import WordCloud
import static.txt.pass2txt as pass2txt
import wc.count_noun as count_noun
from os import path
import wc.count_noun as count_noun

# テキストのサンプル
p = r"C:\Users\nutta\OneDrive\ドキュメント\授業資料\知識形成論：第1回.docx"
text = pass2txt.getwords(p)


# d = path.dirname(__file__)
# text = open(path.join(d, 'sample1.txt')).read()

# Windowsにインストールされているフォントを指定 
wc = WordCloud(
  font_path='C:\Windows\Fonts\yumin.ttf',
  prefer_horizontal = 1,
  background_color = "white",
  # grayでモノクロ、jetでRGB
  colormap = "jet",
  width = 400,
  height = 400,
  font_step = 6,
  min_font_size=6
  )

# ワードクラウドの作成
# wc.generate(text)

# 辞書からワードクラウドを作成
noundict = count_noun.getcount(text)
wc.generate_from_frequencies(noundict[0])

# WindowsパソコンのPドライブ直下に画像を保存
# if wordcloud.colormap == "jet":
#   wordcloud.to_file('wc_rgb.jpg') 
# elif wordcloud.colormap == "gray":
#   wordcloud.to_file('wc_mono.jpg')

# svg変換の参考コード↓
# https://analytics-note.xyz/programming/wordcloud-output-html/

wc.to_svg("wc.svg")

# textタグたちに、クリック時にGoogle検索結果を開くイベントリスナーを追加するJavaScript
link_script = """
<script>
    svg = document.getElementsByTagName("svg")[0];
    text_tags =  svg.getElementsByTagName("text")
    for(var i=0; i<text_tags.length; i++){
        text_tags[i].addEventListener(
            "click",
            function(){
                word = this.textContent;
                console.log(this);
                this.setAttribute("style", "border: 3px solid;");
                word_uri = encodeURI(word);
                url = "https://www.google.com/search?q=" + word_uri;
                window.open(url, "_bkank");

            }
        )
    }
</script>"""

html_script = """
<!DOCTYPE html>\n
"""


# HTMLファイルに書き出し
with open("word_cloud.html", "w", encoding ="utf-8") as f:
    f.write(html_script)
    f.write(wc.to_svg())
    f.write(link_script)

