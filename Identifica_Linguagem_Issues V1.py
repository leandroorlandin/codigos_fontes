import time
import ast
import json
import csv
import numpy as np
import pandas as pd
from langdetect import detect

#IMPRIME O HORÁRIO PARA CONTROLE
def imprime_time():
    localtime = time.localtime()
    result = time.strftime("%I:%M:%S %p", localtime)
    print(result)

#DEFINIÇÃO DOS ARQUIVOS
arquivoentrada = 'arquivoissues_separado_semdupls - V7.4.csv'
arquivosaida = 'arquivoissues_separado_semdupls_language - V7.4.csv'


#DEFINIÇÃO DO DICIONÁRIO DE LEITURA DO ARQUIVO DE ENTRADA
#id;commit;time;encontrado? ;keyword;wcag;message
with open(arquivoentrada, encoding="utf-8") as csv_file_entrada:
    csv_reader = csv.DictReader(csv_file_entrada, delimiter=';', fieldnames=["source_location",
                                                                             "issue",
                                                                             "time",
                                                                             "seencontrado",
                                                                             "tipo",
                                                                             "keyword",
                                                                             "wcag",
                                                                             "titulo",
                                                                             "body"])
    csv_reader.__next__()

# ABERTURA ARQUIVO DE SAIDA
    with open(arquivosaida, mode='w', encoding="utf-8", newline='') as csv_file_saida:
        fieldnames = ["source_location",
                      "issue",
                      "time",
                      "seencontrado",
                      "tipo",
                      "keyword",
                      "wcag",
                      "titulo",
                      "body",
                      "linguagemtitulo",
                      "linguagembody"]
        writer = csv.DictWriter(csv_file_saida, delimiter=';', fieldnames=fieldnames)

        ###############################
        #INICIO DO PROGRAMA
        ###############################
        print("INICIO DO PGM")
        imprime_time()
        total_registros = 0
        registros_loop = 0
        writer.writeheader()

        ###############################
        #INICIO DO LOOP DE LEITURA
        ###############################
        for row in csv_reader:
            total_registros = total_registros + 1
            registros_loop = registros_loop + 1

            ###############################
            #CONTADORES E STATUS
            ###############################
            #if total_registros == 500:
            #    imprime_time()
            #    quit(2)
            if registros_loop == 5000:
                registros_loop = 0
                print("Status Andamento - Registro: ", total_registros)
                imprime_time()

            ###############################
            #VERIFICAÇÃO LINGUAGEM TITULO
            ###############################
            try:
                langtitulo = detect(str(row["titulo"]))
            except:
                langtitulo = "idioma não identificado no titulo"
                #if str(row["body"]) != "":
                #    print("***********")
                #    print("linguagem não identificada no body")
                #    print("url: ",str(row["url"]))
                #    print("body: ",str(row["body"]))
                #    print("***********")

            ###############################
            # VERIFICAÇÃO LINGUAGEM BODY
            ###############################
            try:
                langbody = detect(str(row["body"]))
            except:
                langbody = "idioma não identificado no body"

            linha_saida = row
            linha_saida["linguagemtitulo"] = langtitulo
            linha_saida["linguagembody"] = langbody
            writer.writerow(linha_saida)

        print("FIM DO PGM")
        imprime_time()

'''
#GRAVA HEADER DO ARQUIVO DE SAIDA
linha_header = "#id;commit;time;encontrado? ;keyword;wcag;message;language" + "\n"
arquivo_saida.write(linha_header)

i = 0

#print("tamanho arquivo entrada: ", len(arquivo_entrada))

'''


'''
while i < len(arquivo_entrada):
    i = i + 1

    #PARADA PARA TESTE
    if i == 100:
        quit(2)

    if i == 1:
        break
    print('message: ', message)

'''




'''
    retorno_consulta_json = json.loads(linha)
    totalcommits = totalcommits + len(retorno_consulta_json)
    if i == 5000 or i == 10000 or i == 15000 or i == 20000 or i == 25000:
        print("i = ",i)
        print("totalcommits = ",totalcommits)
        print("saida = ",saida)
        imprime_time()
    linha2 = 0

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