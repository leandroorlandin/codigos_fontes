import time
import ast
import json
import csv
import numpy as np
import pandas as pd

#IMPRIME O HORÁRIO PARA CONTROLE
def imprime_time():
    localtime = time.localtime()
    result = time.strftime("%I:%M:%S %p", localtime)
    print(result)

#DEFINIÇÃO DOS ARQUIVOS
arquivoentrada = 'arquivocommits_separado - V7.4.csv'
arquivosaida = 'arquivocommits_separado_semdupls - V7.4.txt'

#ABERTURA DOS ARQUIVOS
arquivo_entrada = pd.read_csv(arquivoentrada,encoding='utf-8', delimiter=';')
#arquivo_saida = open(arquivosaida, 'w',encoding="utf-8")

print("INICIO DO PGM")
imprime_time()

print('*************')
print('TAMANHO ARQUIVO ENTRADA: ', len(arquivo_entrada))
print('*************')

print('***RETIRADA DA DUPLICIDADE*****')
arquivo_entrada = arquivo_entrada.drop_duplicates()
imprime_time()
arquivo_entrada.to_csv(r'arquivocommits_separado_semdupls - V7.4.csv', sep=';', encoding='utf-8', header='true')
imprime_time()
print('TAMANHO ARQUIVO SAIDA: ', len(arquivo_entrada))

print("FINAL DO PGM")
imprime_time()


'''
print(arquivo_entrada.count())
print('*************')
print(len(arquivo_entrada.index))
print('*************')
print(arquivo_entrada[arquivo_entrada.columns[0]].count())
print('*************')
print(arquivo_entrada.groupby(["wcag"]).size())
print('*************')
print(arquivo_entrada[(arquivo_entrada["tipo"] == "BODY")].count())
#arquivo_saida.write(str(arquivo_entrada.groupby(["wcag"]).size().head(500)))
#arquivodesaida = arquivo_entrada.groupby(["wcag"]).size().head(500)
print('1*************')
'''