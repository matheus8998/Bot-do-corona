# -*- coding: utf-8 -*-  
# encoding: utf-8

import tweepy as tw
import pandas as pd
import time
import datetime
import func
import matplotlib.pyplot as plt
import seaborn as sns

CONSUMER_KEY = 'bR3iHMDhNbdavrlBHaPZlWZpG'
CONSUMER_SECRET = 'lZ1JqlZL2uWEhGsccW5XGVrgj6Lo0zYdlZBdQ36efXkBZjwZXw'
ACCESS_KEY = '734148623064256512-51QfkYCHEPk6X4RTK1LeVLVBoe1YNJn'
ACCESS_SECRET = 'r2RuEFNDf9ntv0CTa8inZ1eIFlgMErcclsegrUAG3UQMM'

auth = tw.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tw.API(auth)	

uri = 'https://raw.githubusercontent.com/wcota/covid19br/master/cases-brazil-states.csv'
FILE_NAME = 'last_seen_id.txt'
MORTES_DIARIAS_GRAF = 'mortes_diarias.png'
MORTES_TOTAIS_GRAF = 'mortes_totais.png'

def recupera_ultimo_id(file_name):
    f_read = open(file_name, 'r')
    last_seen_id = int(f_read.read().strip())
    f_read.close()
    return last_seen_id

def guarda_ultimo_id(ultimo_id, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(ultimo_id))
    f_write.close()
    return

def responde_tweets():
 #   print('retrieving and replying to tweets...', flush=True)
    # DEV NOTE: use 1060651988453654528 for testing.
    ultimo_id = recupera_ultimo_id(FILE_NAME)
    # NOTE: We need to use tweet_mode='extended' below to show
    # all full tweets (with full_text). Without it, long tweets
    # would be cut off.
    mentions = api.mentions_timeline(
                        ultimo_id,
                        tweet_mode='extended')

    for mention in reversed(mentions):
        ultimo_id = mention.id
        guarda_ultimo_id(ultimo_id, FILE_NAME)

        dados = pd.read_csv(uri)
        
        dados.date = pd.to_datetime(dados.date)
        texto_tweet = str(api.mentions_timeline()[0].text)
        uf = func.acha_uf(texto_tweet)

        if  uf != 'TODOS':            
            selecao = (dados.state == uf)
            casos_por_uf = dados[selecao]
            casos_por_uf_geral = casos_por_uf.tail(1)

            ultimas_mortes, penultimas_mortes, antipenultimas_mortes = func.ultimas_mortes(casos_por_uf)
            ultima_data_format, penultima_data_format, antipenultima_data_format = func.ultimos_dias(casos_por_uf) 
            ultimos_casos, penultimos_casos, antipenultimos_casos = func.ultimos_casos(casos_por_uf)
            total_mortes_uf, total_testes_uf, total_casos_uf = func.dados_totais_uf(casos_por_uf_geral)


            func.graficos(casos_por_uf, 'deaths')
            func.graficos(casos_por_uf, 'newDeaths')

            fotos = [MORTES_DIARIAS_GRAF, MORTES_TOTAIS_GRAF]
            media_ids = []
            for foto in fotos:
                res = api.media_upload(foto)
                media_ids.append(res.media_id)

            api.update_status(status = '@' + mention.user.screen_name + '\nMortes em ' + uf + '\n' +
                                  ultima_data_format + ' - ' + ultimas_mortes + '\n' +
                                  penultima_data_format + ' - ' + penultimas_mortes + '\n' +
                                  antipenultima_data_format + ' - ' + antipenultimas_mortes + '\n' +
                                  'Total  - ' + total_mortes_uf + '\n\n' +
                                  'Total de testes - ' +  total_testes_uf + '\n\n' +
                                  'Casos em ' + uf + '\n' +
                                  ultima_data_format + ' - ' + ultimos_casos + '\n' +
                                  penultima_data_format + ' - ' + penultimos_casos + '\n' +
                                  antipenultima_data_format + ' - ' + antipenultimos_casos + '\n' +
                                  'Total  - ' + total_casos_uf, media_ids=media_ids)

while True:
    responde_tweets()
    time.sleep(5)

    