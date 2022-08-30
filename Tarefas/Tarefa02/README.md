# Ferramentas para obtenção de valores através de Expressões Regulares

## Ferramenta 01 - obter e-mails através de uma lista fornecida (e-mails.txt)

### Entrada (e-mails.txt)

    "ALEXANDRE APARECIDO SCROCARO JUNIOR" <alexandre.2001@alunos.utfpr.edu.br>,
    "ANDRE LUCAS MONEGAT COSTA" <andre.monegat@gmail.com>,
    "ARTUR MARCHI PACAGNAN" <marchiartur@gmail.com>,
    "CAIO LEONARDO ARAUJO MIGLIOLI" <caiomiglioli@gmail.com>,
    "CARLOS MIGUEL DOS SANTOS FILHO" <carfil@alunos.utfpr.edu.br>,
    "EVERTON JUNIOR DE ABREU" <evertonabreu@alunos.utfpr.edu.br>,
    "GUILHERME VASCO DA SILVA" <guilhermevasco08@gmail.com>,
    "GUSTAVO KIOSHI ASATO" <gustavoasato@hotmail.com>,
    "HENRIQUE HERCULES LOPES DOS SANTOS" <henriquesantos@alunos.utfpr.edu.br>,
    "JOAO VICTOR NASCIMENTO" <nascimento783@gmail.com>,
    "LEONARDO OMORI FARIAS" <leonardofarias@alunos.utfpr.edu.br>,
    "LUCAS HENRIQUE PEREIRA" <lucashenrique.pereira@hotmail.com>,
    "MATHEUS PATRIARCA SANTANA" <msantana@alunos.utfpr.edu.br>,
    "Prof. Rogério" <rogerioag@professores.utfpr.edu.br>,
    "Prof. Rogério" <rogerioag@utfpr.edu.br>,

### Código desenvolvido

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