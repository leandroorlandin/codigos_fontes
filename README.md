Ordem de execução:

IMPORTANTE: 
Sempre renomear o arquivo de saída "arquivocommits.json" para não correr o risco de perder o mesmo.



OBTENÇÃO DE DADOS:

1 - Executar "ChamadaAPICommits : Vx.py", onde x é a última versão do programa que realiza a busca de dados de Commits.
Entrada 1: "final_sample_data.csv" : lista de aplicativos que possuem versão no Github e no FDroid
Saída 1: "arquivocommits.json" : arquivo com JSONs dos commits
Saída 2: "arquivocommits + nome_arquivo_especifico + .json" :  arquivos com os JSONs de cada app, para facilitar a leitura e manutenção dos dados

2 - Executar "ChamadaAPIIssues - Vx.py", onde x é a última versão do programa que realiza a busca de dados de Issues
Entrada 1: "final_sample_data.csv" : lista de aplicativos que possuem versão no Github e no FDroid
Saída 1: "arquivoissues.json" : arquivo com JSONs dos commits
Saída 2: "arquivoissues + nome_arquivo_especifico + .json" :  arquivos com os JSONs de cada app, para facilitar a leitura e manutenção dos dados



VALIDAÇÃO DOS DADOS

3 - Executar "validaarquivocommits.py"
Caso o mesmo encontrem algum json com problema o programa informará ao final da execução, gravando erros em arquivo "arquivocommitsunificadoerros.json"

4 - Executar "validaarquivoissues.py"
Caso o mesmo encontrem algum json com problema o programa informará ao final da execução, gravando erros em arquivo "arquivoissuesunificadoerros.json"




QUEBRA DOS DADOS E CONFRONTO CONTRA LISTA DE KEYWORDS

5 - Executar "QuebraCommits - Vx.py" para quebrar as informações obtidas nos JSONs em um novo arquivo csv
Entrada 1: "arquivocommits.json" : arquivo com JSONs
Entrada 2: "keywordslist_V2 - sem duplicidades.csv" : contém a lista de palavras chave a serem filtradas
Saída 1: "arquivocommits_separado.txt" : arquivo com informações dos JSONs separadas

6 - Executar "QuebraIssues - Vx.py" para quebrar as informações obtidas nos JSONs em um novo arquivo csv
Entrada 1: "arquivoissues.json" : arquivo com JSONs
Entrada 2: "keywordslist_V2 - sem duplicidades.csv" : contém a lista de palavras chave a serem filtradas
Saída 1: "arquivoissues_separado.txt" : arquivo com informações dos JSONs separadas



RETIRA REGISTROS DUPLICADOS QUE POR VENTURA POSSAM EXISTIR
IMPORTANTE: O Pandas deu erro quando numerou alguns registros. Importante verificar se todos os registros possuem um "id" inicial

7 - Executar "RetiraDuplicados Commits - vx.py" para retirar registros duplicados dos registros que por ventura o Github possa ter entregue
Entrada 1: "arquivocommits_separado.txt" : arquivo com informações dos campos
Saída 1: "arquivocommits_separado_semdupls.csv" : arquivo com informações dos campos sem duplicidade de registros

8 - Executar "RetiraDuplicados Issues - vx.py" para retirar registros duplicados dos registros que por ventura o Github possa ter entregue
Entrada 1: "arquivoissues_separado.txt" : arquivo com informações dos campos
Saída 1: "arquivoissues_separado_semdupls.csv" : arquivo com informações dos campos sem duplicidade de registros



FILTRAR APENAS OS REGISTROS NA LÍNGUA INGLÊS
IMPORTANTE: É necessário revisar se a linguagem foi corretamente preenchida.

9 - Executar "Identifica_Linguagem_Commits Vx.py" para identificar o idioma das mensagens dos Commits
Entrada: "arquivocommits_separado_semdupls.csv" : arquivo com informações dos campos sem duplicidade de registros
Saída: "arquivocommits_separado_semdupls_language.csv" : arquivo com informações do idioma 

10 - Executar "Identifica_Linguagem_Issues Vx.py" para identificar a linguagem dos títulos e descrições das Issues
Entrada: "arquivoissues_separado_semdupls.csv" : arquivo com informações dos campos sem duplicidade de registros
Saída: "arquivoissues_separado_semdupls_language.csv" : arquivo com informações dos campos sem duplicidade de registros



LISTAR OS COMENTARIOS DOS "N" DIRETÓRIOS
IMPORTANTE: No código tem um truncate de string para obter o nome do aplicativo a partir do nome da pasta.
Se o nome da pasta raiz for alterado, este truncate precisa ser revisto.
Código: "diretorio = os.path.dirname(filename)[12:len(os.path.dirname(filename))]"

11 - Executar "Lista_Comentarios_Vx.py" para ler os comentários dos "N" diretórios, cruzar com as palavras chave e gerar um arquivo csv
Entrada 1: Diretório que contém os comentários.
Entrada 2: "keywordslist_V2 - sem duplicidades.csv" : contém a lista de palavras chave a serem filtradas
Saída 1: "arquivocomentarios_separado_Vx.txt" : arquivo com informações dos comentários
Saída 2: "arquivocomentarios_separado_reduzido_Vx.txt" arquivo com informações dos comentários com truncate de 2047 posições. Motivo: tentativa de leitura dos dados no Quicksight da AWS
