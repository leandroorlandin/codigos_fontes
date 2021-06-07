#MUDAR O ARQUIVO DE ENTRADA PARA fdroid_gplay_apps_val.csv
#MUDAR O TIME PARA 62 MIN E 4990 CHAMADAS


import requests
import time
import csv
import numpy as np

#IMPRIME O HORÁRIO PARA CONTROLE
def imprime_time():
    localtime = time.localtime()
    result = time.strftime("%I:%M:%S %p", localtime)
    print(result)

#DEFINIÇÃO DOS ARQUIVOS
arquivoapps = 'final_sample_data.csv'
#arquivoapps = 'final_sample_data - Teste.csv'
arquivoissues = 'arquivoissues.json'

#ABERTURA DOS ARQUIVOS
arquivo_apps = open(arquivoapps, 'r',encoding="utf-8")
arquivo_issues = open(arquivoissues, 'w', encoding="utf-8")

#DEFINIÇÃO DO PAYLOAD E AUTENTICAÇÃO
#https://developer.github.com/v3/#rate-limiting
payload = {}
headers = {
  'Authorization': 'Bearer 87962d1727b8c9f78cd64bb1aed8392c740c5e37'
}

#token sem acessos de manutenção
#nome: token_busca_commits_issues
#token: 87962d1727b8c9f78cd64bb1aed8392c740c5e37
#página do Git que informa como criar um token:
#https://developer.github.com/changes/2020-02-14-deprecating-password-auth/


#DEFINIÇÃO DO DICIONÁRIO DE LEITURA DO ARQUIVO DE ENTRADA
package_name,\
project_name,\
category,\
activities,\
size,\
installs,\
min_installs,\
score,\
ratings,\
reviews,\
release_date,\
fdroid_age_days,\
source_location,\
apk_file,\
src_file,\
download_link=np.loadtxt(arquivoapps,
                            delimiter=',',
                            unpack=True,
                            dtype='str',
                            encoding="utf-8")
linhas = csv.reader(arquivoapps)

#INICIALIZA CONTADOR
i=1
#restarta o processo a partir de um app
#i=74
numero_chamadas = 0
numero_chamadas_total = 0
qtd_regs_saida = 0

#REALIZA LOOP NO ARQUIVO DE ENTRADA
while i < len(source_location):
    if 'https://github.com/' in source_location[i]:
        #print("i = ", i)
        #print(source_location[i])
        # TRATA O NOME DO REPOSITORIO PARA FORMAR A URL DA API DE CONSULTA
        repo = source_location[i]
        #print(repo[19:len(repo)])
        urlissues = "https://api.github.com/repos/" + repo[19:len(repo)] + "/issues?page="
        #print(urlissues)
        nome_arquivo_especifico = repo[19:len(repo)]
        nome_arquivo_especifico = nome_arquivo_especifico.replace("/","")

        #DEFINIÇÃO DO ARQUIVO DE SAÍDA ESPECÍFICO PARA O APP
        arquivoissuesespecifico = "arquivoissues" + nome_arquivo_especifico + ".json"
        arquivo_issues_especifico = open(arquivoissuesespecifico, 'w', encoding="utf-8")

        page = 1
        continua = "S"
        while continua == "S":
            #IF PARA AGUARDAR 62 MINUTOS
            if numero_chamadas == 4960:
            #if numero_chamadas == 10:
                print("inicio do sleep:")
                imprime_time()
                #time.sleep(2 * 3)
                time.sleep(60 * 62)
                print("fim do sleep:")
                imprime_time()
                numero_chamadas = 0

            urlissuescompleta = urlissues + str(page)
            numero_chamadas = numero_chamadas + 1
            numero_chamadas_total = numero_chamadas_total + 1
            print(i, " - ", numero_chamadas, "|", numero_chamadas_total, "|", "urlcompleta = ", urlissuescompleta)
            #REQUEST NA API DE CONSULTA DO GITHUB
            try:
                requisicao_get = requests.request("GET", urlissuescompleta, headers=headers, data = payload)
            except Exception as e:
                print("Requisicao com erro:", requisicao_get.text)
                break
            textoget = requisicao_get.text
            #print(textoget)

            # GRAVA ARQUIVOS DE SAIDA, SE NÃO FOR O FINAL DAS PÁGINAS
            if requisicao_get.status_code == 200 and textoget != "[]":
                qtd_regs_saida = qtd_regs_saida + 1
                arquivo_issues.write(textoget + "\n")
                arquivo_issues_especifico.write(textoget + "\n")
                page = page + 1
            else:
                continua = "N"

            #depois de executar a extração, retirar os registros que tenham retornado sem documentação"
            #{"message":"Not Found","documentation_url":"https://docs.github.com/rest"}
            imprime_time()


    # ADICIONA NO CONTADOR
    i=i+1

print("numero_chamadas_total: ", numero_chamadas_total)