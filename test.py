import pass2txt
import count_noun

p = r"C:\Users\nutta\OneDrive\ドキュメント\授業資料\(学類長・専門学群長宛)平成31年度座長団選出報告書.docx"

p2 = r"C:\Users\nutta\myProject\FileSystem\sample1.txt"

words = pass2txt.getwords(p2)

print(count_noun.getcount(words))