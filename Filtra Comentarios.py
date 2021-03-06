import time
import csv
import numpy as np
import pandas as pd

#IMPRIME O HORÁRIO PARA CONTROLE
def imprime_time():
    localtime = time.localtime()
    result = time.strftime("%I:%M:%S %p", localtime)
    print(result)

print("INICIO DO PGM")
imprime_time()

#DEFINIÇÃO DOS ARQUIVOS
#TESTE:
arquivoentrada = 'arquivocomentarios_semwcag.txt'
#arquivoentrada = 'arquivocomentarios_semwcag_reduzido.txt'
#arquivoentrada = 'arquivocomentarios_semwcag_reduzido-teste.txt'
arquivosaida = 'arquivocomentarios_semwcag_reduzido_filtro.txt'

#ABERTURA DOS ARQUIVOS
arquivo_entrada = pd.read_csv(arquivoentrada,encoding='utf-8', delimiter=';',
                              dtype={"score": "string", "scoretext": "string"})
print("tamanho arquivo entrada antes: ",len(arquivo_entrada))
arquivo_entrada = arquivo_entrada.drop_duplicates()
print("tamanho arquivo entrada depois: ",len(arquivo_entrada))

ruleskeywordsfile = 'rules keywords - v1.csv'

#DEFINIÇÃO DATAFRAME DE SAIDA
filtro = pd.DataFrame(columns =  ["aplicativo",
                                  "url",
                                  "texto",
                                  "score",
                                  "scoretext",
                                  "resposta","data","data_resposta",
                                  "regra"])

#ABERTURA DOS ARQUIVOS
arquivo_entrada_keywords = open(ruleskeywordsfile, 'r',encoding="utf-8")


#DEFINIÇÃO DO DICIONÁRIO DE LEITURA DO ARQUIVO DE ENTRADA DE REGRAS
expressions,\
pandas_expressions,\
id_dir=np.loadtxt(ruleskeywordsfile,
                            delimiter=';',
                            unpack=True,
                            dtype='str',
                            encoding="utf-8")
linhas = csv.reader(ruleskeywordsfile)

#Inicia do 1 para não considerar o header
i = 1

print("INICIO DO LOOP")
imprime_time()

while i < len(pandas_expressions):
    regra = i
    print("****************************************")
    print("lógica: ",expressions[i])
    print('regra:', regra, '- ID_WCAG: ', str(id_dir[i]))
    arquivo_entrada['regra'] = regra
    arquivo_entrada['expression'] = expressions[i]
    arquivo_entrada['WCAG'] = id_dir[i]
    print("comando a ser executado: ", pandas_expressions[i])
    exec('conjunto = '+pandas_expressions[i])
    print('itens selecionados na regra: ', len(conjunto))
    #    print(conjunto)
    filtro = pd.concat([filtro,conjunto])
    print('itens selecionados acumulados: ', len(filtro))
    print("****************************************")
    print("")
    #    print(filtro)
    i = i + 1


'''#while i < len(pandas_expressions):
while i == 49:
    regra = i
    print('regra:', regra, '-', str(pandas_expressions[i]))
    arquivo_entrada['regra'] = regra

    string_filtro = pandas_expressions[i]
    print('1cont',string_filtro)
    print('1tipo', type(string_filtro))
    filtro = pd.concat([arquivo_entrada[arquivo_entrada['texto'].str.contains(string_filtro,
                                                                   case=False,
                                                                   na=False)], filtro])
    print(filtro)


    string_filtro = r'^(?=.*text)(?=.*line)'
    print('2cont', string_filtro)
    print('2tipo', type(string_filtro))
    filtro = pd.concat([arquivo_entrada[arquivo_entrada['texto'].str.contains(string_filtro,
                                                                   case=False,
                                                                   na=False)], filtro])
    print(filtro)


    i = i + 1
'''


print("FIM DO LOOP")
imprime_time()


'''text = [
        ('word1 word2 word3.', 0),
        ('word1 word3 word2.', 0),
        ('word1 word2 word.', 0)
         ]
labels = ['texto','numero']
df = pd.DataFrame.from_records(text, columns=labels)
variavelx = ((df['texto'].str.contains('word1')) | (df['texto'].str.contains('word2'))) & (df['texto'].str.contains('word3'))
df = df[variavelx]
#df  = df[((df['texto'].str.contains('word1')) | (df['texto'].str.contains('word2'))) & (df['texto'].str.contains('word3'))]
print(df)
'''


# GRAVAÇÃO DOS DADOS DE SAÍDA
# arquivo_entrada.to_csv(arquivosaida, sep=';', encoding='utf-8', header='true', index=False)
#print(filtro)
print('tamanho final do conjunto',len(filtro))
filtro.to_csv(arquivosaida, sep=';', encoding='utf-8', header='true', index=False)
print("FIM DO PROGRAMA")
imprime_time()
