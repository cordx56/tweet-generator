# Markov Chain Tweet Generator

Run `$ docker-compose build && docker-compose up`

This program uses [jsvine/markovify](https://github.com/jsvine/markovify) and [MeCab](https://taku910.github.io/mecab/).  
To know all dependencies, see [Pipfile](python/Pipfile) and [Dockerfile](Dockerfile).

## Config & files
Set `django/tweet_generator/local_settings.py`. See below.
```python
DEBUG = False
SECRET_KEY = 'secret'
TWITTER_API_CONKEY = 'API key'
TWITTER_API_CONSEC = 'API key secret'
```

`django/font.ttf`

`nuxt/common.js` is defining `API_BASE_URL`.

## Documentation
https://docs.contour.so/cordx56/tweet-generator/getting-started
