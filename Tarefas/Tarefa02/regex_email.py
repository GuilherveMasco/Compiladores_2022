import re

emails = [] #criação do vetor de emails (caso necessário)
file = open('e-mails.txt','r') #abrir arquivo e-mails.txt

while True:
    line = file.readline() #leitura de linhas do txt

    if not line: #caso fim do txt
        break

    value = line.strip() #valor da linha

    reg = r'\<(.*?)\>' #expressão regular para pegar valor entre < >
    email = re.findall(reg, value)
    print(email[0]) #imprime email
    emails.append(email[0]) #adiciona email à lista
#para imprimir lista, tirar comentário da linha abaixo
#print(emails)