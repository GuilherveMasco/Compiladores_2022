import re

links = [] #criação do vetor de emails (caso necessário)
file = open('test.html','r') #abrir arquivo test.html

while True:
    line = file.readline() #leitura de linhas do txt

    if not line: #caso fim do txt
        break

    value = line.strip() #valor da linha

    reg = r'href=\"http(.*?)\"' #expressão regular para pegar valores de URL
    
    link = re.findall(reg, value)
    if(link): #verifica se houve ocorrência de URL na linha
        link[0] = "http" + link[0] #recupera parte excluída da regex
        print(link[0]) #imprime URL
        links.append(link[0]) #adiciona url à lista
#para imprimir lista, tirar comentário da linha abaixo
#print(links)