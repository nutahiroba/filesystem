import json

with open("tfdict.json", "r", encoding="utf-8") as f:
    tfdict = json.load(f)

with open("dfdict.json", "r", encoding="utf-8") as f:
    dfdict = json.load(f)

# tf値上位ソート
tfdict = {k: v for k, v in sorted(tfdict.items(), key=lambda x: x[1], reverse=True)}

# df値上位ソート
dfdict = {k: v for k, v in sorted(dfdict.items(), key=lambda x: x[1], reverse=True)}

for k, v in tfdict.items():
    if v > 50:
        print(k, v)

for k, v in dfdict.items():
    if v > 10:
        print(k, v)

