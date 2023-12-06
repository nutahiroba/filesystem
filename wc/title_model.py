# https://github.com/neologd/mecab-ipadic-neologd/wiki/Regexp.ja から引用・一部改変
from __future__ import unicode_literals
import re
import unicodedata
import torch
from torch.utils.data import Dataset, DataLoader
from transformers import T5ForConditionalGeneration, T5Tokenizer
from transformers import AdamW, get_linear_schedule_with_warmup

# 学習済みモデルをHugging Face model hubからダウンロードする
model_dir_name = "sonoisa/t5-qiita-title-generation"

# トークナイザー（SentencePiece）
tokenizer = T5Tokenizer.from_pretrained(model_dir_name, is_fast=True)

# 学習済みモデル
trained_model = T5ForConditionalGeneration.from_pretrained(model_dir_name)

# GPUの利用有無
USE_GPU = torch.cuda.is_available()
if USE_GPU:
    trained_model.cuda()


def unicode_normalize(cls, s):
    pt = re.compile("([{}]+)".format(cls))

    def norm(c):
        return unicodedata.normalize("NFKC", c) if pt.match(c) else c

    s = "".join(norm(x) for x in re.split(pt, s))
    s = re.sub("－", "-", s)
    return s


def remove_extra_spaces(s):
    s = re.sub("[ 　]+", " ", s)
    blocks = "".join(
        (
            "\u4E00-\u9FFF",  # CJK UNIFIED IDEOGRAPHS
            "\u3040-\u309F",  # HIRAGANA
            "\u30A0-\u30FF",  # KATAKANA
            "\u3000-\u303F",  # CJK SYMBOLS AND PUNCTUATION
            "\uFF00-\uFFEF",  # HALFWIDTH AND FULLWIDTH FORMS
        )
    )
    basic_latin = "\u0000-\u007F"

    def remove_space_between(cls1, cls2, s):
        p = re.compile("([{}]) ([{}])".format(cls1, cls2))
        while p.search(s):
            s = p.sub(r"\1\2", s)
        return s

    s = remove_space_between(blocks, blocks, s)
    s = remove_space_between(blocks, basic_latin, s)
    s = remove_space_between(basic_latin, blocks, s)
    return s


def normalize_neologd(s):
    s = s.strip()
    s = unicode_normalize("０-９Ａ-Ｚａ-ｚ｡-ﾟ", s)

    def maketrans(f, t):
        return {ord(x): ord(y) for x, y in zip(f, t)}

    s = re.sub("[˗֊‐‑‒–⁃⁻₋−]+", "-", s)  # normalize hyphens
    s = re.sub("[﹣－ｰ—―─━ー]+", "ー", s)  # normalize choonpus
    s = re.sub("[~∼∾〜〰～]+", "〜", s)  # normalize tildes (modified by Isao Sonobe)
    s = s.translate(
        maketrans(
            "!\"#$%&'()*+,-./:;<=>?@[¥]^_`{|}~｡､･｢｣",
            "！”＃＄％＆’（）＊＋，－．／：；＜＝＞？＠［￥］＾＿｀｛｜｝〜。、・「」",
        )
    )

    s = remove_extra_spaces(s)
    s = unicode_normalize("！”＃＄％＆’（）＊＋，－．／：；＜＞？＠［￥］＾＿｀｛｜｝〜", s)  # keep ＝,・,「,」
    s = re.sub("[’]", "'", s)
    s = re.sub("[”]", '"', s)
    return s


import re

CODE_PATTERN = re.compile(r"```.*?```", re.MULTILINE | re.DOTALL)
LINK_PATTERN = re.compile(r"!?\[([^\]\)]+)\]\([^\)]+\)")
IMG_PATTERN = re.compile(r"<img[^>]*>")
URL_PATTERN = re.compile(r"(http|ftp)s?://[^\s]+")
NEWLINES_PATTERN = re.compile(r"(\s*\n\s*)+")


def clean_markdown(markdown_text):
    markdown_text = CODE_PATTERN.sub(r"", markdown_text)
    markdown_text = LINK_PATTERN.sub(r"\1", markdown_text)
    markdown_text = IMG_PATTERN.sub(r"", markdown_text)
    markdown_text = URL_PATTERN.sub(r"", markdown_text)
    markdown_text = NEWLINES_PATTERN.sub(r"\n", markdown_text)
    markdown_text = markdown_text.replace("`", "")
    return markdown_text


def normalize_text(markdown_text):
    markdown_text = clean_markdown(markdown_text)
    markdown_text = markdown_text.replace("\t", " ")
    markdown_text = normalize_neologd(markdown_text).lower()
    markdown_text = markdown_text.replace("\n", " ")
    return markdown_text


def preprocess_qiita_body(markdown_text):
    return "body: " + normalize_text(markdown_text)[:4000]


def postprocess_title(title):
    return re.sub(r"^title: ", "", title)


qiita_body = """
デジタル庁への入庁に係る諸手続等について
R5.11.17

・宿舎希望の有無【対象：４月入庁者全員、早期入庁者は現時点で該当なし】
【１月15日（月）まで】宿舎希望の有無をお知らせ下さい。
　みなさん必ず宿舎希望の有無をご返信ください。
回答は以下のformsからお願いいたします。
https://forms.office.com/r/kmF5RHrHeY

・赴任旅費の対象か否か【対象：４月入庁者全員、早期入庁者は現時点で該当なし】
　赴任旅費の対象となるか否かについても【１月15日（月）まで】にお知らせ下さい。
　回答は以下のformsからお願いいたします。
　https://forms.office.com/r/mMng0SRFLZ
　　※赴任旅費の対象になるかどうかは別添を参照願います。

・給与の格付け【対象：４月入庁者全員、早期入庁者は現時点で該当なし】
　学生は卒業証明書、既卒者は卒業証明書（＋就業証明書（職歴がある場合））の提出を、２月29日（木）までにお願いします。
なお、現役の学生・院生に関しては学校によって締め切りまでの提出が難しいことが想定
されるため、３月22日（金）〆切とします。
また、院生の場合、院卒の証明書類（修了証明書）を提出いただければ、学部の卒業証明書は不要です。

・健康であることの証明書類【対象：全員】
以下を満たす健康診断書を２月29日（木）までにご提出をお願いいたします。
　（検査項目）身長、体重、腹囲、BMI、視力、聴力、血圧、検尿、胸部X線、所見が含まれているもの。
　なお、既に実施した健康診断で上記を満たしている場合は、新たに受診していただく必要はありませんので、該当の健康診断書の提出をお願いいたします。


・給与、共済関係の書類【対象：全員】
入庁の２週間前（４月入庁の場合は、３月15日（金））までに御提出をお願いします。
　なお、早期入庁者は１週間前までに御提出をお願いします。
事前提出が必要な書類は、別添「提出書類一覧」Ｇ列「○」印のついた様式５～６-別紙、８、様式１２～１４です。
申請日は発令日以降となりますが、通常時より共済組合員証の交付に相当時間がかかるため、事前に書類を提出願います。
※所属欄は空欄で差し支えありません。

・本籍地を証明できる書類【対象：全員】
住民票を取得する際に本籍地の記載を選択できると思われますので、本籍地記載の住民票の写しの提出で差し支えありません【３月22日（金）〆】
※上記締め切りまでに提出が難しい場合は、入庁後の提出で差し支えありません。

"""


def get_title(qiita_body):
    # preprocess_qiita_body(qiita_body)

    MAX_SOURCE_LENGTH = 2048  # 入力される記事本文の最大トークン数
    MAX_TARGET_LENGTH = 64  # 生成されるタイトルの最大トークン数

    # 推論モード設定
    trained_model.eval()

    # 前処理とトークナイズを行う
    inputs = [preprocess_qiita_body(qiita_body)]
    batch = tokenizer.batch_encode_plus(
        inputs,
        max_length=MAX_SOURCE_LENGTH,
        truncation=True,
        padding="longest",
        return_tensors="pt",
    )

    input_ids = batch["input_ids"]
    input_mask = batch["attention_mask"]
    if USE_GPU:
        input_ids = input_ids.cuda()
        input_mask = input_mask.cuda()

    # 生成処理を行う
    outputs = trained_model.generate(
        input_ids=input_ids,
        attention_mask=input_mask,
        max_length=MAX_TARGET_LENGTH,
        return_dict_in_generate=True,
        output_scores=True,
        temperature=1.0,  # 生成にランダム性を入れる温度パラメータ
        num_beams=10,  # ビームサーチの探索幅
        diversity_penalty=1.0,  # 生成結果の多様性を生み出すためのペナルティ
        num_beam_groups=5,  # ビームサーチのグループ数
        num_return_sequences=1,  # 生成する文の数
        repetition_penalty=1.5,  # 同じ文の繰り返し（モード崩壊）へのペナルティ
    )

    # 生成されたトークン列を文字列に変換する
    generated_titles = [
        tokenizer.decode(
            ids, skip_special_tokens=True, clean_up_tokenization_spaces=False
        )
        for ids in outputs.sequences
    ]

    # 生成されたタイトルを表示する
    # for i, title in enumerate(generated_titles):
    #     print(f"{i+1:2}. {postprocess_title(title)}")
    return postprocess_title(generated_titles[0])


# print(get_title(qiita_body))
