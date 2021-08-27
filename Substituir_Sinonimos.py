import time
import ast
import json
import csv
import numpy as np
import pandas as pd
import re

#IMPRIME O HORÁRIO PARA CONTROLE
def imprime_time():
    localtime = time.localtime()
    result = time.strftime("%I:%M:%S %p", localtime)
    print(result)

print("INICIO DO PGM")
imprime_time()

#DEFINIÇÃO DOS ARQUIVOS
arquivoentradarules = 'rules keywords - v2.csv'
arquivoentradasinonimos = 'sinonimos.csv'
arquivosaidarules = 'rules keywords com sinonimos.csv'

#ABERTURA DOS ARQUIVOS
arquivo_entrada_rules = open(arquivoentradarules, 'r',encoding="utf-8")
arquivo_entrada_sinonimos  = open(arquivoentradasinonimos, 'r',encoding="utf-8")
arquivosaidarules = open(arquivosaidarules, 'w',encoding="utf-8")

#DEFINIÇÃO DO DICIONÁRIO DE LEITURA DO ARQUIVO DE ENTRADA DE REGRAS
ID,\
Expressions,\
Pandas_Expressions,\
ID_DIR,\
Qtd_Words=np.loadtxt(arquivoentradarules,
                            delimiter=';',
                            unpack=True,
                            dtype='str',
                            encoding="utf-8")
linhas_rules = csv.reader(arquivoentradarules)

#DEFINIÇÃO DO DICIONÁRIO DE LEITURA DO ARQUIVO DE ENTRADA DE REGRAS
ID_Sinonimo,\
Word,\
Sinonimo=np.loadtxt(arquivoentradasinonimos,
                            delimiter=';',
                            unpack=True,
                            dtype='str',
                            encoding="utf-8")
linhas_sinonimos = csv.reader(arquivoentradasinonimos)

numero_linhas_ent_rules = 0
numero_linhas_sai = 0
numero_linhas_erros = 0


for linhas_rules in arquivo_entrada_rules:
    print("linhas_rules = ",linhas_rules)
    if numero_linhas_ent_rules == 0:
        linha_completa = "ID;ID_Sinonimo;Expressions;Pandas_Expressions;ID_DIR;Qtd_Words\n"
    else:
        #grava linha igual à da entrada, antes das alterações
        #arquivosaidarules.write(linhas_rules)
        linha_completa = str(ID[numero_linhas_ent_rules]) + ";" + \
                         "0" + ";" + \
                         str(Expressions[numero_linhas_ent_rules]) + ";" + \
                         str(Pandas_Expressions[numero_linhas_ent_rules]) + ";" + \
                         str(ID_DIR[numero_linhas_ent_rules]) + ";" + \
                         str(Qtd_Words[numero_linhas_ent_rules]) + "\n"
        #print("linha_completa = ", linha_completa)
    arquivosaidarules.write(linha_completa)
    numero_linhas_sai = numero_linhas_sai + 1


#FALTA FAZER O LOOP DE N SINONIMOS!!!!!


    #realiza loops de verificação de sinonimos
    i=0
    while i < len(Sinonimo):
        if Word[i] in Pandas_Expressions[numero_linhas_ent_rules]:
            texto_alterado = str(Pandas_Expressions[numero_linhas_ent_rules]).replace(Word[i],Sinonimo[i])
            linha_completa = str(ID[numero_linhas_ent_rules]) + ";" + \
                             str(ID_Sinonimo[i]) + ";" + \
                             str(Expressions[numero_linhas_ent_rules]) + ";" + \
                             texto_alterado + ";" + \
                             str(ID_DIR[numero_linhas_ent_rules]) + ";" + \
                             str(Qtd_Words[numero_linhas_ent_rules]) + "\n"
            print("linha_completa = ",linha_completa)
            arquivosaidarules.write(linha_completa)
            numero_linhas_sai = numero_linhas_sai + 1
        i = i + 1

    numero_linhas_ent_rules = numero_linhas_ent_rules + 1

print("FIM DO PGM")
imprime_time()





'''
#DAQUI PARA BAIXO FOI A V1 - ALTERAÇÃO DE PALAVRAS CONSIDERANDO APENAS 1 OCORRÊNCIA NO TEXTO


for linhas_rules in arquivo_entrada_rules:
    print("linhas_rules = ",linhas_rules)
    if numero_linhas_ent_rules == 0:
        linha_completa = "ID;ID_Sinonimo;Expressions;Pandas_Expressions;ID_DIR;Qtd_Words\n"
    else:
        #grava linha igual à da entrada, antes das alterações
        #arquivosaidarules.write(linhas_rules)
        linha_completa = str(ID[numero_linhas_ent_rules]) + ";" + \
                         "0" + ";" + \
                         str(Expressions[numero_linhas_ent_rules]) + ";" + \
                         str(Pandas_Expressions[numero_linhas_ent_rules]) + ";" + \
                         str(ID_DIR[numero_linhas_ent_rules]) + ";" + \
                         str(Qtd_Words[numero_linhas_ent_rules]) + "\n"
        #print("linha_completa = ", linha_completa)
    arquivosaidarules.write(linha_completa)
    numero_linhas_sai = numero_linhas_sai + 1


#FALTA FAZER O LOOP DE N SINONIMOS!!!!!


    #realiza loops de verificação de sinonimos
    i=0
    while i < len(Sinonimo):
        if Word[i] in Pandas_Expressions[numero_linhas_ent_rules]:
            texto_alterado = str(Pandas_Expressions[numero_linhas_ent_rules]).replace(Word[i],Sinonimo[i])
            linha_completa = str(ID[numero_linhas_ent_rules]) + ";" + \
                             str(ID_Sinonimo[i]) + ";" + \
                             str(Expressions[numero_linhas_ent_rules]) + ";" + \
                             texto_alterado + ";" + \
                             str(ID_DIR[numero_linhas_ent_rules]) + ";" + \
                             str(Qtd_Words[numero_linhas_ent_rules]) + "\n"
            print("linha_completa = ",linha_completa)
            arquivosaidarules.write(linha_completa)
            numero_linhas_sai = numero_linhas_sai + 1
        i = i + 1

    numero_linhas_ent_rules = numero_linhas_ent_rules + 1

print("FIM DO PGM")
imprime_time()

'''