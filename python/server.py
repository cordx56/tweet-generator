#!/usr/bin/env python3
import os
import sys
import datetime
import markovify
from flask import Flask, request, redirect, abort, jsonify
import urllib.parse
import MeCab
import exportModel
from twitterTools import TwitterTools

app = Flask(__name__)

twitterKeys = { "CK": os.environ.get("TWITTER_API_CONKEY"), "CS": os.environ.get("TWITTER_API_CONSEC") }

mec = MeCab.Tagger("-d /usr/lib/mecab/dic/mecab-ipadic-neologd -O wakati")


# Twitter related pages
@app.route("/pyapi/tw/authLink")
def twitterAuthLink():
    global twitterKeys
    if "callback" not in request.args:
        abort(400)
    twt = TwitterTools(twitterKeys["CK"], twitterKeys["CS"], None, None, request.args["callback"])
    return redirect(twt.getAuthenticateURL())

@app.route("/pyapi/tw/authAndGen")
def twitterAuthAndGen():
    global twitterKeys
    successMsg = None
    errMsg = None
    try:
        twt = TwitterTools(twitterKeys["CK"], twitterKeys["CS"], None, None)
        twt.oauth.parse_authorization_response(request.url)
        token = twt.oauth.fetch_access_token("https://api.twitter.com/oauth/access_token")
        twt = TwitterTools(twitterKeys["CK"], twitterKeys["CS"], token["oauth_token"], token["oauth_token_secret"])
        params = { "screen_name": token["screen_name"], "trim_user": 1 }
        filepath = os.path.join("./chainfiles", token["screen_name"].lower() + ".json")
        if (os.path.isfile(filepath) and datetime.datetime.now().timestamp() - os.path.getmtime(filepath) < 60 * 60 * 24):
            errMsg = "You can generate Markov chain only once per 24 hours."
        else:
            exportModel.generateAndExport(exportModel.loadTwitterAPI(twt, params), filepath)
            successMsg = token["screen_name"] + "'s Markov chain model was successfully GENERATED!"
    except Exception as e:
        print(e)
        errMsg = "Failed to generate your Markov chain. Please retry a few minutes later."
    if successMsg:
        return redirect("https://markov.cordx.net/" + token["screen_name"] + "?success=" + urllib.parse.quote(successMsg))
    else:
        return redirect("https://markov.cordx.net/?error=" + urllib.parse.quote(errMsg))


# main api
@app.route("/pyapi/genText/<screenName>", methods = ["GET", "POST"])
def textGen(screenName = None):
    if screenName is None:
        return jsonify({ "status": False, "message": "ScreenName not specified!" }), 400
    screenName = os.path.basename(screenName).lower()
    if screenName[0] == '@':
        screenName = screenName[1:]
    if request.method == "POST" and request.json is None:
        return jsonify({ "status": False, "message": "Invalid request." }), 400
    if not os.path.isfile("./chainfiles/" + screenName + ".json"):
        return jsonify({ "status": False, "message": "Leaned model file not found. まずはじめにツイートを学習させてください。" }), 404
    try:
        with open("./chainfiles/" + screenName + ".json") as f:
            textModel = markovify.Text.from_json(f.read())
        reqJson = request.json
        if reqJson is not None and reqJson["startWith"] and 0 < len(reqJson["startWith"].strip()):
            startWithStr = mec.parse(reqJson["startWith"]).strip().split()
            if textModel.state_size < len(startWithStr):
                startWithStr = startWithStr[0:textModel.state_size]
            startWithStr = " ".join(startWithStr)
            try:
                sentence = textModel.make_sentence_with_start(startWithStr, tries = 100)
            except KeyError:
                return jsonify({ "status": False, "message": "生成失敗。該当開始語が存在しません。" }), 500
        elif reqJson is not None and str(reqJson["length"]).isdecimal():
            sentence = textModel.make_short_sentence(int(reqJson["length"]), tries = 100)
        else:
            sentence = textModel.make_sentence(tries = 100)
        print("@" + screenName + ", Request: " + str(reqJson) + ", Sentence:" + "".join(str(sentence)))  # Log
        if sentence is not None:
            sentence = "".join(sentence.split())
            tweetLink = 'https://twitter.com/intent/tweet?text=' + urllib.parse.quote(sentence) + \
                '&url=' + urllib.parse.quote("https://markov.cordx.net/" + screenName)
            return jsonify({ "status": True, "sentence": sentence, "tweetLink": tweetLink })
        else:
            return jsonify({ "status": False, "message": "生成失敗。複数回試してみてください。" }), 500
    except Exception as e:
        print(e)
        return jsonify({ "status": False, "message": "Unknown error." }), 500


if __name__ == "__main__":
    port = 5000
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    app.run(host = "0.0.0.0", port = port)
