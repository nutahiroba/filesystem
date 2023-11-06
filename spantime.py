import docx

path = r'C:\Users\nutta\OneDrive\ドキュメント\授業資料\(学類長・専門学群長宛)平成31年度座長団選出報告書.docx'

obj = docx.opc.coreprops.CoreProperties(path)

print(obj.revision)