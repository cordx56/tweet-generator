#!/usr/bin/env python3
import json
from requests_oauthlib import OAuth1Session


class TwitterTools:
    oauth = None
    def __init__(self, ck, cs, at = None, ats = None, callback = None):
        self.oauth = OAuth1Session(ck, cs, at, ats, callback)


    def requestToken(self):
        url = "https://api.twitter.com/oauth/request_token"
        return self.oauth.fetch_request_token(url)

    def getAuthenticateURL(self):
        url = "https://api.twitter.com/oauth/authenticate"
        self.requestToken()
        return self.oauth.authorization_url(url)


    def fetchTweets(self, params):
        url = "https://api.twitter.com/1.1/statuses/user_timeline.json"
        req = self.oauth.get(url, params = params)
        if req.status_code != 200:
            raise TwitterAPIError(req)
        return json.loads(req.text)


    def fetchTweetsLoop(self, params, loop):
        tweets = []
        params["count"] = 200
        params["include_rts"] = 1
        for i in range(loop):
            req = self.fetchTweets(params)
            if len(req) < 2:
                tweets.extend(req)
                break
            tweets.extend(req[:-1])
            params["max_id"] = req[-1]["id"]
        return tweets

class TwitterAPIError(Exception):
    def __init__(self, req):
        self.req = req
    def __str__(self):
        return str(self.req.status_code)
