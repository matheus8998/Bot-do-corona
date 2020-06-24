# -*- coding: utf-8 -*- 
# encoding: utf-8

import tweepy as tw
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

ufs = ['AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT',
       'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 'RS', 'RO',
       'RR', 'SC', 'SP', 'SE', 'TO']
TODOS = 'TODOS'
MORTES_DIARIAS_GRAF = 'mortes_diarias.png'
MORTES_TOTAIS_GRAF = 'mortes_totais.png'


def acha_uf(texto_tweet):
	texto_tweet_list = str(texto_tweet).upper().split()
	print(texto_tweet_list)

	uf_selecionada = TODOS

	for uf in ufs:
		if uf in texto_tweet_list:
			uf_selecionada = uf
			break
	print(uf_selecionada)		
	return uf_selecionada

# uf = acha_uf('teste de sp')
# print(uf)

def ultimas_mortes(casos_por_uf):
  ult_situacao, penul_situacao, antipenul_situacao = ultimas_situacoes(casos_por_uf)

  ult_morte = ult_situacao.newDeaths.to_string().split()[1]
  penul_morte = penul_situacao.newDeaths.to_string().split()[1]
  antipenul_morte = antipenul_situacao.newDeaths.to_string().split()[1]

  return ult_morte, penul_morte, antipenul_morte

def ultimos_casos(casos_por_uf):
  ult_situacao, penul_situacao, antipenul_situacao = ultimas_situacoes(casos_por_uf)
  
  ult_caso = ult_situacao.newCases.to_string().split()[1]
  penul_caso = penul_situacao.newCases.to_string().split()[1]
  antipenul_caso = antipenul_situacao.newCases.to_string().split()[1]

  return ult_caso, penul_caso, antipenul_caso

def ultimos_dias(casos_por_uf):
  ult_situacao, penul_situacao, antipenul_situacao = ultimas_situacoes(casos_por_uf)
  
  ultima_data_string = ult_situacao.date.to_string().split()[1].split('-')
  penultima_data_string = penul_situacao.date.to_string().split()[1].split('-')
  antipenultima_data_string = antipenul_situacao.date.to_string().split()[1].split('-')

  ult_data_fm = ultima_data_string[2] + '/' + ultima_data_string[1]
  penul_data_fm = penultima_data_string[2] + '/' + penultima_data_string[1]
  antipenul_data_fm = antipenultima_data_string[2] + '/' + antipenultima_data_string[1]

  return ult_data_fm, penul_data_fm, antipenul_data_fm

def dados_totais_uf(casos_por_uf_geral):
  total_mortes = casos_por_uf_geral.deaths.to_string().split()[1]
  total_testes = casos_por_uf_geral.tests.to_string().split()[1]
  total_casos  = casos_por_uf_geral.totalCases.to_string().split()[1]

  return total_mortes, total_testes, total_casos

def graficos(casos_por_uf, variavel_y):
  plt.figure(figsize=(15, 10))
  ax = sns.lineplot(x="date", y=variavel_y, data=casos_por_uf)
  for ind, label in enumerate(ax.get_xticklabels()):
    if ind % 10 == 0:  # every 10th label is kept
      label.set_visible(True)
    else:
      label.set_visible(False)

  if variavel_y == 'deaths':     
    plt.title(u"Numero total de mortes")
    plt.ylabel(u'Mortes')
    plt.xlabel(u'Data')
    plt.savefig(MORTES_DIARIAS_GRAF)
  elif variavel_y == 'newDeaths':
    plt.title(u"Numero de novas mortes por dia")
    plt.ylabel(u'Mortes diarias')
    plt.xlabel(u'Data')
    plt.savefig(MORTES_TOTAIS_GRAF)



def ultimas_situacoes(casos_por_uf):
  ultima_data = casos_por_uf.date.max()
  penultima_data = ultima_data - pd.to_timedelta(1, unit='d')
  antipenultima_data = ultima_data - pd.to_timedelta(2, unit='d')
 
  ultima_situacao = casos_por_uf[casos_por_uf.date==ultima_data]
  penultima_situacao = casos_por_uf[casos_por_uf.date==penultima_data]
  antipenultima_situacao = casos_por_uf[casos_por_uf.date==antipenultima_data]

  return ultima_situacao, penultima_situacao, antipenultima_situacao