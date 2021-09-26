FROM python:3.8

RUN apt-get update && \
    apt-get install -y mecab libmecab-dev mecab-ipadic-utf8 swig
#RUN git clone --depth=1 https://github.com/neologd/mecab-ipadic-neologd && \
#    cd ./mecab-ipadic-neologd && \
#    ./bin/install-mecab-ipadic-neologd -y -p /var/lib/mecab/dic/mecab-ipadic-neologd && \
#    rm -rf ./mecab-ipadic-neologd
RUN ln -s /var/lib/mecab/dic /usr/lib/mecab/dic

WORKDIR /app
COPY Pipfile .
COPY Pipfile.lock .
RUN pip install pipenv && \
    pipenv install --system
COPY . .

CMD gunicorn -c /app/gunicorn.py tweet_generator.wsgi
