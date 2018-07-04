#!/usr/bin/env python
# encoding: utf-8

import tweepy

consumer_key = ''
consumer_secret = ''

access_token = ''
access_token_secret = ''

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

api.get_user('@UserName')

nuevos_tweets = api.user_timeline(screen_name = 'UserName',count=200, tweet_mode="extended")
lista_tweets = [[tweet.full_text] for tweet in nuevos_tweets]


import csv
import codecs

# La siguiente función está basada en https://gist.github.com/yanofsky/5436496
def get_all_tweets(screen_name):
    # Twitter deja descargar alrededor de 3200 tweets con este método

    # Autorizar a Twitter:
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    # Inicializar una lista vacía para almacenar los tweets.
    alltweets = []

    # Request inicial (últimos 200 tweets):
    new_tweets = api.user_timeline(screen_name=screen_name, count=200, tweet_mode="extended")

    # Guardar los últimos tweets:
    alltweets.extend(new_tweets)

    # Guardar el id del último tweet, menos uno (penúltimo tweet):
    oldest = alltweets[-1].id - 1

    # Continuar guardando tweets hasta que no quede ninguno:
    while len(new_tweets) > 0:
        print("Descargando tweets anteriores al id %s" % (oldest))

        # all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name=screen_name, count=200, max_id=oldest, tweet_mode="extended")

        # save most recent tweets
        alltweets.extend(new_tweets)

        # update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1

        print("...%s tweets descargados hasta ahora" % (len(alltweets)))

    # Transformar alltweets en un arreglo 2D para popular el csv:
    outtweets = [[tweet.id_str, tweet.created_at, tweet.full_text] for tweet in alltweets]

    # Escribir el csv
    ENCODING = 'utf-8'
    with codecs.open('%s_tweets.csv' % screen_name, 'w', ENCODING) as f:
        writer = csv.writer(f)
        writer.writerow(["id", "Fecha y hora", "Texto"])
        writer.writerows(outtweets)

    pass
    return outtweets


if __name__ == '__main__':
    # pass in the username of the account you want to download
    get_all_tweets("UserName")
