# 辞書orテキストからwcをsvgで作成
from wordcloud import WordCloud

def get(words):

  wc = WordCloud(
    font_path = 'C:\Windows\Fonts\yumin.ttf',
    prefer_horizontal = 1,
    background_color = "white",
    # grayでモノクロ、jetでRGB
    colormap = "jet",
    width = 600,
    height = 600,
    # font_stepが動作しない
    # font_step = 25,
    min_font_size=15,
    )
  
  if type(words) == dict:
    wc.generate_from_frequencies(words)
  elif type(words) == str:
    wc.generate_from_text(words)
  else:
    print("This is unravaliable")
    return None
  
  return wc