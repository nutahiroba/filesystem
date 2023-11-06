import pass2txt
import count_noun
from nltk.corpus import stopwords
import nltk
import make_wc
from docx import Document
import pathlib

# .docxファイルを開く

p = pathlib.Path(r"C:\Users\nutta\OneDrive\ドキュメント\授業資料")
docs_list = list(p.glob("*.docx"))
# p = r'C:\Users\nutta\OneDrive\ドキュメント\授業資料\(学類長・専門学群長宛)平成31年度座長団選出報告書.docx'


with open("metadata.txt", "w", encoding="utf-8") as f:
    for file in docs_list:
        doc = Document(file)  # ファイル名を実際のファイル名に置き換える
        title = str(file).split("\\")[-1]

        # メタデータを取得
        metadata = {
            'Title':title,
            # 'Title': doc.core_properties.title,
            # 'Author': doc.core_properties.author,
            # 'Subject': doc.core_properties.subject,
            # 'Keywords': doc.core_properties.keywords,
            # 'Comments': doc.core_properties.comments,
            # 'Last Modified By': doc.core_properties.last_modified_by,
            'Revision': doc.core_properties.revision,
            'Created': doc.core_properties.created,
            'Modified': doc.core_properties.modified,
        }

        # メタデータを表示
        for key, value in metadata.items():
            print(f'{key}: {value}', file = f)
        print("-" * 20, file = f)

# make_wc.get({"a":10})

# with open("stopword.txt", "r",encoding="utf-8") as f:
#   stopwords = f.readlines()

# stopwords = [string.strip() for string in stopwords if string.strip()]

# for word in stopwords:
#   print(word)

# nltk.download('stopwords')
# stop_words = stopwords.words('english')
# print(stop_words)

# stoppath = "Japanese.txt"
# with open(stoppath, "r", encoding= "utf-8") as f:
#   stopwords = f.readlines()

# # nltkモジュールから取得したstopwords
# with open("English.txt", "r", encoding="utf-8") as f:
#   en_stopwords = f.readlines()

# en_sw = en_stopwords[0].replace(",|[|]| ", "")
# for word in en_sw.split(","):
#   stopwords.append(word[2:-1])

# stopwords = [string.strip() for string in stopwords if string.strip()]

# print(stopwords)

# p = r"C:\Users\nutta\OneDrive\ドキュメント\授業資料\(学類長・専門学群長宛)平成31年度座長団選出報告書.docx"

# p2 = r"C:\Users\nutta\myProject\FileSystem\sample1.txt"

# words = pass2txt.getwords(p2)

# print(count_noun.getcount(words))


# stoppath = "Japanese.txt"
# with open(stoppath, "r", encoding = "utf-8") as f:
#   stopwords = f.readlines()

# stopwords = [string.strip() for string in stopwords if string.strip()]
# print(stopwords[:3])


    # svg = document.getElementsByTagName("svg")[0];
    # text_tags =  svg.getElementsByTagName("text")
    # for(var i=0; i<text_tags.length; i++){
    #     text_tags[i].addEventListener(
    #         "click",
    #         function(){
    #             word = this.textContent;
    #             console.log(this);
    #             this.setAttribute("style", "border: 3px solid;");
    #             word_uri = encodeURI(word);
    #             url = "https://www.google.com/search?q=" + word_uri;
    #             window.open(url, "_bkank");

    #         }
    #     )
    # }