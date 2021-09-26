# Markov Chain Tweet Generator

Run `$ docker-compose build && docker-compose up`

This program uses [jsvine/markovify](https://github.com/jsvine/markovify) and [MeCab](https://taku910.github.io/mecab/).  
To know all dependencies, see [Pipfile](python/Pipfile) and [Dockerfile](Dockerfile).

## Config & files
Set `django/tweet_generator/local_settings.py`. See below.
```python
DEBUG = False
SECRET_KEY = 'secret'
POSTGRES_DB = 'Your DB name in PostgreSQL'
POSTGRES_USER = 'Your username in PostgreSQL'
POSTGRES_PASSWORD = 'Your password in PostgreSQL'
POSTGRES_HOST = 'postgres'
WEBPAGE_BASE_URL = 'localhost:3000'
TWITTER_API_CONKEY = 'API key'
TWITTER_API_CONSEC = 'API key secret'
```

`django/font.ttf`

`nuxt/common.js` is defining `API_BASE_URL`.
