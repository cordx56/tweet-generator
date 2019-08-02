#!/usr/bin/env python3
import sys
import re
import pandas
import MeCab
import markovify

mecabW = MeCab.Tagger("-d /usr/lib/mecab/dic/mecab-ipadic-neologd -O wakati")


def filterTweets(twts):
    replyMatch = re.compile(r"@\w+")
    urlMatch = re.compile(r"https?://")
    data = []
    for text in twts:
        if replyMatch.search(text) or urlMatch.search(text):
            continue
        data.append(text)
    return data


def loadTwitterCSV(filepath):
    data = pandas.read_csv(filepath)
    return "\n".join(filterTweets(data["text"]))


def loadTwitterAPI(twt, params):
    tweets = twt.fetchTweetsLoop(params, 100)
    text = [s["text"] for s in tweets if "retweeted_status" not in s]
    return "\n".join(filterTweets(text))


def generateAndExport(src, dest, state_size = 3):
    src = src.replace("?", "？").replace("!", "！").replace("，", "、").replace("．", "。").replace("。", "。\n")
    data = [mecabW.parse(s) for s in src.split("\n") if s != ""]
    joinedData = "".join(data)
    modeljson = markovify.NewlineText(joinedData, state_size = state_size).to_json()
    with open(dest, mode = "w") as f:
        f.write(modeljson)
    return len(data)


if __name__ == "__main__":
    if len(sys.argv) > 3:
        learned = generateAndExport(loadTwitterCSV(sys.argv[1]), sys.argv[2], int(sys.argv[3]))
    else:
        learned = generateAndExport(loadTwitterCSV(sys.argv[1]), sys.argv[2])
    print("Exported " + str(learned) + " lines learned data to " + sys.argv[2] + ".")
