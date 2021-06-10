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
arquivoentrada = 'arquivoissues_separado - V7.4.csv'
arquivosaida = 'arquivoissues_separado_semdupls - V7.4.txt'

print("INICIO DO PGM")
imprime_time()

#ABERTURA DOS ARQUIVOS
arquivo_entrada = pd.read_csv(arquivoentrada,encoding='utf-8', delimiter=';')
#arquivo_saida = open(arquivosaida, 'w',encoding="utf-8")


print('*************')
print('TAMANHO ARQUIVO ENTRADA: ', len(arquivo_entrada))
print('*************')

print('***RETIRADA DA DUPLICIDADE*****')
arquivo_entrada = arquivo_entrada.drop_duplicates()
imprime_time()
#arquivo_entrada.to_csv(r'arquivoissues_separado_semdupls - V7.4.csv', sep=';', encoding='utf-8', header='true')
arquivo_entrada.to_csv(arquivosaida, sep=';', encoding='utf-8', header='true', index=False)
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