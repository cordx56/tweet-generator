import json

def fetch_tweets(oauth, params):
    url = "https://api.twitter.com/1.1/statuses/user_timeline.json"
    req = oauth.get(url, params=params)
    if req.status_code != 200:
        raise TwitterAPIError(req)
    return json.loads(req.text)

def fetch_tweets_loop(oauth, params, loop):
    tweets = []
    params["count"] = 200
    params["include_rts"] = 1
    for i in range(loop):
        req = fetch_tweets(oauth, params)
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
