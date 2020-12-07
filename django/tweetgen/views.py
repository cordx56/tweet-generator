# from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from account.models import User
from django.contrib.auth import login
from django.shortcuts import redirect
from django.http import FileResponse
from .models import GeneratedModel

import logging
from datetime import datetime
import urllib
from requests_oauthlib import OAuth1Session
import MeCab
import markovify

# Image draw
import io
from PIL import Image, ImageDraw, ImageFont

from . import generate_model

logger = logging.getLogger('django')
mec = MeCab.Tagger("-r /dev/null -d /usr/lib/mecab/dic/mecab-ipadic-neologd -O wakati")

class AuthRedirectAPIView(APIView):
    def get(self, request):
        if 'callback' not in request.query_params:
            return Response(
                {
                    'message': 'callback URL not specified!'
                },
                status.HTTP_400_BAD_REQUEST
            )
        oauth = OAuth1Session(settings.TWITTER_API_CONKEY, settings.TWITTER_API_CONSEC, None, None, request.query_params['callback'])
        oauth.fetch_request_token("https://api.twitter.com/oauth/request_token")
        url = oauth.authorization_url("https://api.twitter.com/oauth/authenticate")
        return redirect(url)

def twitter_fetch_token(request):
    oauth = OAuth1Session(settings.TWITTER_API_CONKEY, settings.TWITTER_API_CONSEC, None, None)
    oauth.parse_authorization_response(request.build_absolute_uri())
    token = oauth.fetch_access_token("https://api.twitter.com/oauth/access_token")
    return token

class AuthAndGenAPIView(APIView):
    def get(self, request):
        try:
            token = twitter_fetch_token(request)
        except Exception as e:
            logger.warning(e)
            return redirect('/?error_unknown')
        oauth_token = token["oauth_token"]
        oauth_token_secret = token["oauth_token_secret"]
        oauth = OAuth1Session(settings.TWITTER_API_CONKEY, settings.TWITTER_API_CONSEC, oauth_token, oauth_token_secret)
        twitter_id = int(token['user_id'])
        screen_name = token['screen_name']

        try:
            tuser = oauth.get('https://api.twitter.com/1.1/users/show.json?screen_name=' + screen_name)
        except Exception as e:
            logger.warning(e)
            return redirect('/?error_unknown')
        is_protected = tuser.json()['protected']

        if User.objects.filter(screen_name=screen_name).exists():
            user = User.objects.get(screen_name=screen_name)
            if user.twitter_id != twitter_id:
                User.objects.filter(screen_name=screen_name).delete()
        if User.objects.filter(twitter_id=twitter_id).exists():
            user = User.objects.get(twitter_id=twitter_id)
            user.screen_name = screen_name
            user.is_protected = is_protected
            # don't save oauth token
            # user.access_token = oauth_token
            # user.access_token_secret = oauth_token_secret
            user.save()
            login(request, user)
        else:
            user = User.objects.create_user(screen_name, twitter_id, is_protected)
            # don't save oauth token
            # user.access_token = oauth_token
            # user.access_token_secret = oauth_token_secret
            user.save()
            login(request, user)

        if GeneratedModel.objects.filter(user=user).exists():
            genmodel = GeneratedModel.objects.get(user=user)
            if datetime.now().timestamp() - genmodel.date.timestamp() < 60 * 60 * 24:
                return redirect('/?error_24hour_constraint')
            GeneratedModel.objects.filter(user=user).delete()

        # Generate model
        params = { "screen_name": screen_name, "trim_user": 1 }
        try:
            model = generate_model.generate_from_tweets(oauth, params)
        except Exception as e:
            logger.warning(e)
            return redirect('/?error_unknown')
        modeljson = model.to_json()
        genmodel = GeneratedModel()
        genmodel.user = user
        genmodel.model = modeljson
        genmodel.save()

        return redirect('/' + screen_name + '?successfully_generated')

class AuthAndDelAPIView(APIView):
    def get(self, request):
        try:
            token = twitter_fetch_token(request)
        except Exception as e:
            logger.warning(e)
            return redirect('/?error_unknown')
        twitter_id = int(token['user_id'])
        if User.objects.filter(twitter_id=twitter_id).exists():
            user = User.objects.get(twitter_id=twitter_id)
            if GeneratedModel.objects.filter(user=user).exists():
                GeneratedModel.objects.filter(user=user).delete()
                return redirect('/' + '?successfully_deleted')
        return redirect('/' + '?error_unregistered')

class GenTextAPIView(APIView):
    def get(self, request, screen_name):
        screen_name = screen_name.lstrip('@')
        if User.objects.filter(screen_name=screen_name).exists():
            user = User.objects.get(screen_name=screen_name)
        else:
            return Response(
                {
                    'status': False,
                    'message': 'Learned model file not found. まずはじめにツイートを学習させてください。'
                },
                status.HTTP_404_NOT_FOUND
            )
        if user.is_protected and (not request.user.is_authenticated or request.user.id != user.id):
            return Response(
                {
                    'status': False,
                    'message': '鍵アカウントでテキストを生成する場合、ログインが必要です。アカウントの持ち主のみが生成可能です。'
                },
                status.HTTP_401_UNAUTHORIZED
            )
        if GeneratedModel.objects.filter(user=user).exists():
            model = GeneratedModel.objects.get(user=user)
        else:
            return Response(
                {
                    'status': False,
                    'message': 'Learned model file not found. まずはじめにツイートを学習させてください。'
                },
                status.HTTP_404_NOT_FOUND
            )
        markov = markovify.Text.from_json(model.model)
        if request.query_params.get('startWith') and 0 < len(request.query_params['startWith'].strip()):
            startWithStr = mec.parse(request.query_params['startWith']).strip().split()
            if markov.state_size < len(startWithStr):
                startWithStr = startWithStr[0:markov.state_size]
            startWithStr = " ".join(startWithStr)
            try:
                text = markov.make_sentence_with_start(startWithStr, tries=100)
            except KeyError:
                return Response(
                    {
                        'status': False,
                        'message': '生成失敗。該当開始語が存在しません。'
                    },
                    status.HTTP_400_BAD_REQUEST
                )
        elif request.query_params.get('length') and str(request.query_params['length']).isdecimal() and 0 < int(request.query_params['length']):
            text = markov.make_short_sentence(int(request.query_params['length']), tries=100)
        else:
            text = markov.make_sentence(tries=100)

        text = "".join(text.split())
        logger.info('TEXTGEN:@{}:{}'.format(screen_name, text))
        if text is None:
            return Response(
                {
                    'status': False,
                    'message': '生成失敗。複数回試してみてください。'
                },
                status.HTTP_400_BAD_REQUEST
            )
        tweet_link = 'https://twitter.com/intent/tweet?text=' + urllib.parse.quote(text + ' #tweetgen') + \
            '&url=' + urllib.parse.quote(settings.WEBPAGE_BASE_URL + '/' + screen_name)
        return Response(
            {
                'status': True,
                'text': text,
                'tweetLink': tweet_link,
            }
        )


def add_text_to_image(img, text, font_size, font_color, max_length=1000):
    font = ImageFont.truetype("font.ttf", font_size)
    draw = ImageDraw.Draw(img)
    if draw.textsize(text, font=font)[0] > max_length:
        while draw.textsize(text + '…', font=font)[0] > max_length:
            text = text[:-1]
        text = text + '…'
    w, h = img.size
    position = (w / 2 - draw.textsize(text, font=font)[0] / 2, 300)
    draw.text(position, text, font_color, font=font)

    return img

class GenImageAPIView(APIView):
    def get(self, request, screen_name=None):
        if screen_name is None:
            screen_name = ''
        screen_name = screen_name.lstrip('@')
        img = Image.open('twittercard.png')
        add_text_to_image(img, '@' + screen_name, 100, (255, 0, 0))
        file_obj = io.BytesIO()
        img.save(file_obj, 'PNG')
        file_obj.seek(0)
        fr = FileResponse(file_obj)
        fr['Content-Type'] = 'image/PNG'
        return fr
