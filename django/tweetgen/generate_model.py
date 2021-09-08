import re
import MeCab
import markovify

from . import twitter_tools

mecabW = MeCab.Tagger("-r /dev/null -d /usr/lib/mecab/dic/ipadic-utf8 -O wakati")

def filter_tweets(twts):
    replyMatch = re.compile(r"@\w+")
    urlMatch = re.compile(r"https?://")
    data = []
    for text in twts:
        if replyMatch.search(text) or urlMatch.search(text):
            continue
        data.append(text)
    return data

def get_tweets_for_generate(oauth, params):
    tweets = twitter_tools.fetch_tweets_loop(oauth, params, 1000)
    text = [s["text"] for s in tweets if "retweeted_status" not in s]
    return "\n".join(filter_tweets(text))

def generate(src, state_size=3):
    src = src.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")
    data = [mecabW.parse(s) for s in src.split("\n") if s != ""]
    joinedData = "".join(data)
    modeljson = markovify.NewlineText(joinedData, state_size=state_size)
    return modeljson

def generate_from_tweets(oauth, params):
    return generate(get_tweets_for_generate(oauth, params))
