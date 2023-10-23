import pathlib
import datetime

def get_ts(filepass):
  st = pathlib.Path.stat(filepass)
  # 最終アクセス時間
  a_dt = datetime.datetime.fromtimestamp(st.st_atime)
  # strftimeで日付、時刻→ストリング
  access_t = a_dt.strftime('%Y年%m月%d日 %H:%M:%S')
  # 最終更新時間
  m_dt = datetime.datetime.fromtimestamp(st.st_mtime)
  make_t = m_dt.strftime('%Y年%m月%d日 %H:%M:%S')
  c_dt = datetime.datetime.fromtimestamp(st.st_ctime)
  create_t = m_dt.strftime('%Y年%m月%d日 %H:%M:%S')

  return make_t