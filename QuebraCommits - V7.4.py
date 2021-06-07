import time
import json
import csv
import numpy as np


#IMPRIME O HORÁRIO PARA CONTROLE
def imprime_time():
    localtime = time.localtime()
    result = time.strftime("%I:%M:%S %p", localtime)
    print(result)



#PESQUISA WORDLIST NAS MESSAGES
def pesquisa_keywords(message):
    j = 0
    quantidade_encontrada = 0
    encontrado = "Encontrado"
    while j < len(keyword):
        if keyword[j] in message:
            registro_completo = url + ";" + data + ";" + encontrado + ";" + keyword[j] + ";" + wcag[j] + ";" + \
                                mensagem + "\n"
            arquivo_commits_separado.write(registro_completo)
            quantidade_encontrada = quantidade_encontrada + 1
        j = j + 1
    return quantidade_encontrada

#DEFINIÇÃO DOS ARQUIVOS
arquivocommitsjson = 'arquivocommits - V1.json'
#ARQUIVO DE TESTE
#arquivocommitsjson = 'arquivocommitstheblackwidowerKanaQuiz.json'
#arquivocommitsseparado = 'arquivocommits_separado.txt'
arquivocommitsseparado = 'arquivocommits_separado - V7.4.csv'
keywordsfile = 'keywordslist_V2 - sem duplicidades.csv'


#ABERTURA DOS ARQUIVOS
arquivo_commits_json = open(arquivocommitsjson, 'r',encoding="utf-8")
arquivo_commits_separado = open(arquivocommitsseparado, 'w',encoding="utf-8")
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
linha_header = "commit" + ";" + "time" + ";" + "encontrado? " + ";" + "keyword" + ";" + "wcag" + ";" + "message" + "\n"
arquivo_commits_separado.write(linha_header)

i = 0
saida = 0
encontrados = 0
naoencontrados = 0
totalcommits = 0
descarte = 0

for linha in arquivo_commits_json:
    i = i + 1
    retorno_consulta_json = json.loads(linha)
    totalcommits = totalcommits + len(retorno_consulta_json)
    if i == 5000 or i == 10000 or i == 15000 or i == 20000 or i == 25000:
        print("i = ",i)
        print("totalcommits = ",totalcommits)
        print("saida = ",saida)
        imprime_time()
    linha2 = 0
    while linha2 < len(retorno_consulta_json):
        commit = retorno_consulta_json[linha2]
        commit['commit']['message'] = commit['commit']['message'].strip('\n')
        url = commit['commit']['url']
        data = commit['commit']['committer']['date']
        mensagem = commit['commit']['message']

        if len(mensagem) > 25000:
            mensagem = "DESCARTE-TAMANHO"
            descarte = descarte + 1

        mensagem = mensagem.replace(";","|")
        mensagem = mensagem.replace("\t", "|")
        mensagem = mensagem.replace("\n","|")
        mensagem = mensagem.replace("\r","|")

        #PESQUISA SE ENCONTRA NO TEXTO DO COMMIT
        seencontrado = pesquisa_keywords(mensagem)
        encontrados = encontrados + seencontrado
        saida = saida + seencontrado

        #TRATA SE NÃO ENCONTRA NO TEXTO DO COMMIT
        if seencontrado == 0:
            registro_completo = url + ";" + data + ";" + "Nao Encontrado" + ";" + "" + ";" + "" + ";" + mensagem + "\n"
            arquivo_commits_separado.write(registro_completo)
            saida = saida + 1
            naoencontrados = naoencontrados + 1
        #INCREMENTA O NÚMERO DE LINHAS DE ENTRADA
        linha2 = linha2 + 1

#FINALIZAÇÃO DO PROGRAMA:

# TOTALIZADORES
print("")
print("###TOTALIZADORES###")
print("TOTAL DE LINHAS DE ENTRADA = ",i)
print("TOTAL DE LINHAS DE GRAVADAS = ",saida)
print("PALAVRAS ENCONTRADAS = ",encontrados)
commitscompalavras = totalcommits - naoencontrados
print("COMMITS SEM PALAVRAS ENCONTRADAS = ", naoencontrados)
print("TOTAL DE COMMITS = ", totalcommits)
print("TOTAL COMMITS COM PALAVRAS ENCONTRADAS = ", commitscompalavras)
print("DESCARTES = ", descarte)
print("FIM DO PGM")

imprime_time()