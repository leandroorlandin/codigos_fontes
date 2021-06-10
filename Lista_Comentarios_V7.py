import time
import time
import ast
import os
from pathlib import Path
import csv
import numpy as np
import fnmatch


# IMPRIME O HORÁRIO PARA CONTROLE
def imprime_time():
    localtime = time.localtime()
    result = time.strftime("%I:%M:%S %p", localtime)
    print(result)

#PESQUISA WORDLIST NOS TEXTOS
def pesquisa_keywords(tipo,message):
    j = 1   #para não considerar o header do arquivo de keywords
    quantidade_encontrada = 0
    while j < len(keyword):
        if keyword[j] in message:
            #registro_completo = str(linha_json_str) + ";" + "Encontrado" + ";" + tipo + ";" + keyword[j] + ";" + wcag[j] + "\n"
            registro_completo = diretorio + ";" + \
                                str(linha_json['url']) + ";" + \
                                str(texto) + ";" + \
                                str(linha_json['score']) + ";" + \
                                str(linha_json['scoreText']) + ";" + \
                                str(resposta) + ";" + \
                                "Encontrado" + ";" + tipo + ";" + keyword[j] + ";" + wcag[j] + "\n"
            arquivo_comentarios_separado.write(registro_completo)

            registro_completo_reduzido = diretorio + ";" + \
                                str(linha_json['url']) + ";" + \
                                str(textoreduzido) + ";" + \
                                str(linha_json['score']) + ";" + \
                                str(linha_json['scoreText']) + ";" + \
                                str(respostareduzido) + ";" + \
                                "Encontrado" + ";" + tipo + ";" + keyword[j] + ";" + wcag[j] + "\n"
            arquivo_comentarios_separado_reduzido.write(registro_completo_reduzido)


            quantidade_encontrada = quantidade_encontrada + 1
        j = j + 1
    return quantidade_encontrada


print("começo do processamento")
imprime_time()

#VARIÁVEIS DE INICIALIZAÇÃO E CONTROLES
pasta = 'allreviews'
#pasta = 'allreviews_teste'
contagem_displays = 500

#NOMES DE ARQUIVOS
arquivocomentariosseparado = 'arquivocomentarios_separado_V7.txt'
arquivocomentariosseparadoreduzido = 'arquivocomentarios_separado_reduzido_V7.txt'
keywordsfile = 'keywordslist_V2 - sem duplicidades.csv'

#ABERTURA DOS ARQUIVOS
arquivo_comentarios_separado = open(arquivocomentariosseparado, 'w',encoding="utf-8")
arquivo_comentarios_separado_reduzido = open(arquivocomentariosseparadoreduzido, 'w',encoding="utf-8")
arquivo_entrada_keywords = open(keywordsfile, 'r',encoding="utf-8")

#DEFINIÇÃO DO DICIONÁRIO DE LEITURA DO ARQUIVO DE ENTRADA
keyword,wcag=np.loadtxt(keywordsfile,
                            delimiter=';',
                            unpack=True,
                            dtype='str',
                            encoding="utf-8")
linhas = csv.reader(keywordsfile)


#DISPLAYS INICIAIS
pastas_aplicacoes = os.listdir(pasta)
print("pasta com todas as reviews: ", pasta)
print("pastas das aplicações: ", pastas_aplicacoes)
print("total de aplicações: ", len(pastas_aplicacoes) - 1)

#CONTADORES DE LINHAS E ARQUIVOS
numero_linhas_total = 0
numero_arquivos_total = 0
saida = 0
encontrados = 0
naoencontrados = 0

print("*********************************")
print("***INICIO DO LOOP DOS ARQUIVOS***")
print("*********************************")



#LOOP DE ARQUIVOS
for filename in Path(pasta).rglob("*.txt"):

    #PRINT DO ENDEREÇO E NOME DO ARQUIVO
    #print("filename: ", filename)


    #ATUALIZA OS CONTADORES
    numero_arquivos_total = numero_arquivos_total + 1
    numero_linhas_arquivo = 0

    #ABERTURA DO ARQUIVO
    arquivoreviewssentrada = str(filename)
    arquivo_reviews_entrada = open(arquivoreviewssentrada, 'r', encoding="utf-8")

    diretorio = os.path.dirname(filename)[12:len(os.path.dirname(filename))]

    #LOOP DE LINHAS DENTRO DE CADA ARQUIVO
    for linha in arquivo_reviews_entrada:
        numero_linhas_arquivo = numero_linhas_arquivo + 1
        numero_linhas_total = numero_linhas_total + 1
        linha_json = ast.literal_eval(linha)

        #TRANSFORMA LINHA DO JSON EM STRING PARA GRAVAÇÃO EM ARQUIVO CSV
        linha_json_str = str(linha_json)
        linha_json_str = linha_json_str.replace(";","|")
        linha_json_str = linha_json_str.replace("\t","|")
        linha_json_str = linha_json_str.replace("\n", "|")
        linha_json_str = linha_json_str.replace("\r","|")

        #EXIBIÇÃO DE LINHA PARA INVESTIGAÇÃO DE ERROS
        #print("\t" , "linha_json " , numero_linhas_arquivo , ": " , linha_json)

        #TRATA TEXTO DO COMENTARIO
        if linha_json['text'] is None:
            texto = ""
        else:
            linha_json['text'] = linha_json['text'].strip('\n')
            texto = linha_json['text']
        texto = texto.replace(";","|")
        texto = texto.replace("\t","|")
        texto = texto.replace("\n", "|")
        texto = texto.replace("\r","|")
        textoreduzido = str(texto)[1:2046]
        # EXIBIÇÃO DE LINHA PARA INVESTIGAÇÃO DE ERROS
        #print("texto: ", texto)

        #TRATA RESPOSTA DO COMENTARIO
        if linha_json['replyText'] is None:
            resposta = ""
        else:
            linha_json['replyText'] = linha_json['replyText'].strip('\n')
            resposta = linha_json['replyText']
        resposta = resposta.replace(";","|")
        resposta = resposta.replace("\t","|")
        resposta = resposta.replace("\n", "|")
        resposta = resposta.replace("\r","|")
        respostareduzido = str(resposta)[1:2046]
        # EXIBIÇÃO DE LINHA PARA INVESTIGAÇÃO DE ERROS
        #print("resposta: ", resposta)

        #PESQUISA SE ENCONTRA NO TEXTO E NA RESPOSTA
        seencontrado_texto = pesquisa_keywords("TEXTO",texto)
        saida = saida + seencontrado_texto
        seencontrado_resposta = pesquisa_keywords("RESPOSTA",resposta)
        saida = saida + seencontrado_resposta

        encontrados = encontrados + seencontrado_texto + seencontrado_resposta

        #TRATA SE NÃO ENCONTRA NEM NO TEXTO E NEM NA RESPOSTA
        if seencontrado_texto == 0 and seencontrado_resposta == 0:
            #print('pasta: ', diretorio)
            #print('pasta: ',os.path.dirname(filename),' tamanho do caminho:', len(os.path.dirname(filename)))
            registro_completo = diretorio + ";" + \
                                str(linha_json['url']) + ";" + \
                                str(texto) + ";" + \
                                str(linha_json['score']) + ";" + \
                                str(linha_json['scoreText']) + ";" + \
                                str(resposta) + ";" + \
                                "Não Encontrado" + ";" + "" + ";" + "" + ";" + "" + "\n"
#            registro_completo = str(linha_json_str) + ";" + "Não Encontrado" + ";" + "" + ";" + "" + ";" + "" + "\n"
            arquivo_comentarios_separado.write(registro_completo)

            registro_completo_reduzido = diretorio + ";" + \
                                str(linha_json['url']) + ";" + \
                                str(textoreduzido) + ";" + \
                                str(linha_json['score']) + ";" + \
                                str(linha_json['scoreText']) + ";" + \
                                str(respostareduzido) + ";" + \
                                "Não Encontrado" + ";" + "" + ";" + "" + ";" + "" + "\n"
            #            registro_completo = str(linha_json_str) + ";" + "Não Encontrado" + ";" + "" + ";" + "" + ";" + "" + "\n"
            arquivo_comentarios_separado_reduzido.write(registro_completo_reduzido)

            saida = saida + 1
            naoencontrados = naoencontrados + 1

        #print("saida: ", saida)
        #print("encontrados: ", encontrados)

        #linha_impressa = str(linha_json)+ ";" + str(linha_json['text']) + ";" + str(linha_json['replyText']) + "\n"
        #arquivo_comentarios_separado.write(linha_impressa)
        #PARADA PARA AGILIZAR TESTES
        if numero_linhas_total == 600:
           quit(-2)

    #FECHAMENTO DO ARQUIVO
    arquivo_reviews_entrada.close()

    #DISPLAY DE CONTROLE DE ARQUIVOS PROCESSADOS
    if numero_arquivos_total % contagem_displays == 0:
        print("numero_de linhas processadas : ", numero_linhas_total)
        print("número de arquivos processados: ", numero_arquivos_total)
        imprime_time()


#ENCERRAMENTO DO PROGRAMA
print("*********************************")
print("***FINAL DO LOOP DOS ARQUIVOS***")
print("*********************************")


#TOTALIZADORES
print("")
print("###TOTALIZADORES###")
print("TOTAL DE ARQUIVOS DE ENTRADA = ", numero_arquivos_total)
print("TOTAL DE LINHAS DE ENTRADA (COMENTARIOS) = ", numero_linhas_total)
print("TOTAL DE LINHAS DE GRAVADAS (PALAVRAS ENCONTRADAS) = ", saida)
print("TOTAL DE PALAVRAS ENCONTRADAS = ", encontrados)
comentarioscompalavras = numero_linhas_total - naoencontrados
print("COMENTARIOS SEM PALAVRAS ENCONTRADAS = ", naoencontrados)
print("TOTAL COMENTARIOS COM PALAVRAS ENCONTRADAS = ", comentarioscompalavras)
print("FIM DO PGM")


print("final do processamento")
imprime_time()

'''
contagem testes:
Total de registros: 783 registros
150 - a2dp.Vol_1.txt
131 - a2dp.Vol_2.txt
046 - aarddict.android_1.txt
150 - acr.browser.lightning_1.txt
150 - acr.browser.lightning_2.txt
150 - acr.browser.lightning_3.txt
006 - acr.browser.lightning_4.txt
'''
