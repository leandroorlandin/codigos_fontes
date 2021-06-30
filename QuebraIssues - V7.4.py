import time
import ast
import json
import csv
import numpy as np


#IMPRIME O HORÁRIO PARA CONTROLE
def imprime_time():
    localtime = time.localtime()
    result = time.strftime("%I:%M:%S %p", localtime)
    print(result)



#PESQUISA WORDLIST NAS MESSAGES
def pesquisa_keywords(tipo,message):
    j = 0
    quantidade_encontrada = 0
    encontrado = "Encontrado"
    while j < len(keyword):
        if keyword[j] in message:
            registro_completo = source_location + ";" + \
                                url + ";" + data + ";" + encontrado + ";" + tipo + ";" + keyword[j] + ";" + wcag[j] + \
                                ";" + titulo + ";" + body + "\n"
            arquivo_issues_separado.write(registro_completo)
            quantidade_encontrada = quantidade_encontrada + 1
        j = j + 1
    return quantidade_encontrada

#DEFINIÇÃO DOS ARQUIVOS
arquivoissuesjson = 'arquivoissues - V1.json'
#arquivoissuesjson = 'arquivoissues - validado - teste.json'
#arquivoissuesseparado = 'arquivoissues_separado.txt'
arquivoissuesseparado = 'arquivoissues_separado - V7.4.csv'
keywordsfile = 'keywordslist_V2 - sem duplicidades.csv'


#ABERTURA DOS ARQUIVOS
arquivo_issues_json = open(arquivoissuesjson, 'r',encoding="utf-8")
arquivo_issues_separado = open(arquivoissuesseparado, 'w',encoding="utf-8")
arquivo_entrada_keywords = open(keywordsfile, 'r',encoding="utf-8")


#DEFINIÇÃO DO DICIONÁRIO DE LEITURA DO ARQUIVO DE ENTRADA
keyword,wcag=np.loadtxt(keywordsfile,
                            delimiter=';',
                            unpack=True,
                            dtype='str',
                            encoding="utf-8")
linhas = csv.reader(keywordsfile)


print("INICIO DO PGM")
imprime_time()

#GRAVA HEADER DO ARQUIVO DE SAIDA
linha_header = "source_location" + ";" + "issue" + ";" + "time" + ";" + "seencontrado" + ";" + "tipo" + ";" + \
               "keyword" + ";" + "wcag" + ";" + "titulo" + ";" + "body" + "\n"
arquivo_issues_separado.write(linha_header)


i = 0
saida = 0
encontrados = 0
naoencontrados = 0
totalissues = 0

for linha in arquivo_issues_json:
    i = i + 1

    #retorno_consulta_json = ast.literal_eval(linha)
    retorno_consulta_json = json.loads(linha)
    totalissues = totalissues + len(retorno_consulta_json)
    if i == 500 or i == 1000 or i == 1500 or i == 2000 or i == 2500:
        print("i = ",i)
        print("totalissues = ",totalissues)
        print("saida = ",saida)
        imprime_time()
    linha2 = 0
    while linha2 < len(retorno_consulta_json):
        issue = retorno_consulta_json[linha2]

        auxiliar = issue['repository_url']
        #print("source location depois: ", auxiliar)
        auxiliar = auxiliar.replace("api.", "")
        auxiliar = auxiliar.replace("repos/", "")
        #print("source location depois: ", auxiliar)
        source_location = auxiliar

        url = issue['url']
        data = issue['created_at']

        #TRATA TITLE DA ISSUE
        issue['title'] = issue['title'].strip('\n')
        titulo = issue['title']

        if len(titulo) > 25000:
            titulo = "DESCARTE-TAMANHO"

        titulo = titulo.replace(";","|")
        titulo = titulo.replace("\t","|")
        titulo = titulo.replace("\n","|")
        titulo = titulo.replace("\r","|")

        #TRATA BODY DA ISSUE
        if issue['body'] is None:
            body = ""
        else:
            issue['body'] = issue['body'].strip('\n')
            body = issue['body']

        #DESCARTE POR TAMANHO DA MENSAGEM
        if len(body) > 25000:
            body = "DESCARTE-TAMANHO"

        body = body.replace(";","|")
        body = body.replace("\t","|")
        body = body.replace("\n", "|")
        body = body.replace("\r","|")

        #PESQUISA SE ENCONTRA NO TITULO E NO BODY
        seencontrado = pesquisa_keywords("TITULO",titulo)
        saida = saida + seencontrado
        seencontrado_body = pesquisa_keywords("BODY",body)
        saida = saida + seencontrado_body

        encontrados = encontrados + seencontrado_body + seencontrado

        #TRATA SE NÃO ENCONTRA NEM NO TITULO NEM NO BODY
        if seencontrado == 0 and seencontrado_body == 0:
            registro_completo = source_location + ";" + \
                                url + ";" + data + ";" + "Não Encontrado" + ";" + "" + ";" + "" + ";" + "" + ";" + \
                                titulo + ";" + body + "\n"
            arquivo_issues_separado.write(registro_completo)
            saida = saida + 1
            naoencontrados = naoencontrados + 1

        #INCREMENTA O NÚMERO DE LINHAS DE ENTRADA
        linha2 = linha2 + 1

        #IF PARA TESTE - PARADA APÓS 1000 REGISTROS GRAVADOS
        #if saida > 1000:
        #    quit(-2)

#FINALIZAÇÃO DO PROGRAMA:

#TOTALIZADORES
print("")
print("###TOTALIZADORES###")
print("TOTAL DE LINHAS DE ENTRADA = ",i)
print("TOTAL DE LINHAS DE GRAVADAS = ",saida)
print("PALAVRAS ENCONTRADAS = ",encontrados)
issuescompalavras = totalissues - naoencontrados
print("ISSUES SEM PALAVRAS ENCONTRADAS = ", naoencontrados)
print("TOTAL DE ISSUES = ", totalissues)
print("TOTAL ISSUES COM PALAVRAS ENCONTRADAS = ", issuescompalavras)
print("FIM DO PGM")

imprime_time()