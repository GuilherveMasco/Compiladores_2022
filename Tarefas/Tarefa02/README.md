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

### Resultado obtido
    alexandre.2001@alunos.utfpr.edu.br
    andre.monegat@gmail.com
    marchiartur@gmail.com
    caiomiglioli@gmail.com
    carfil@alunos.utfpr.edu.br        
    evertonabreu@alunos.utfpr.edu.br  
    guilhermevasco08@gmail.com        
    gustavoasato@hotmail.com
    henriquesantos@alunos.utfpr.edu.br
    nascimento783@gmail.com
    leonardofarias@alunos.utfpr.edu.br
    lucashenrique.pereira@hotmail.com
    msantana@alunos.utfpr.edu.br
    rogerioag@professores.utfpr.edu.br
    rogerioag@utfpr.edu.br


## Ferramenta 02 - obter todos os links (URL) de uma página HTML fornecida (test.html)

### Entrada (test.html)
A entrada utilizada foi o site: https://puginarug.com (Acessado em 30/08/2022)


    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>The Pug In A Rug</title>
    <meta
    name="description"
    content="Watch the Pug be in the Rug. Level up and maximize!"/>

    <!-- Facebook -->
    <meta property="og:title" content="The Pug in the Rug" />
    <meta property="og:url" content="https://puginarug.com/" />
    <meta property="og:site_name" content="The Pug in the Rug" />
    <meta property="og:type" content="website" />
    <meta
        property="og:description"
        content="Watch the Pug be in the Rug. Level up and maximize the amount of pug in your life."
    />

    <meta
        property="og:image"
        content="https://puginarug.com/assets/share.png"
    />
    <meta property="og:url" content="https://puginarug.com/" />
    <meta
        name="twitter:image"
        content="https://puginarug.com/assets/share.png"
    />

    <!-- Twitter -->
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="The Pug in the Rug" />
    <meta name="twitter:url" content="https://puginarug.com" />
    <meta
        name="twitter:description"
        content="Watch the Pug be in the Rug. Level up and maximize the amount of pug in your life."
    />

    <style>
        body, html {
        margin: 0;
        padding: 0;
        max-width: 100vw;
        max-height: 100vh;
        }

        .timer {
        position: fixed;
        bottom: 15px;
        left: 50%;
        transform: translateX(-50%);
        font-family: monospace;
        width: 250px;
        text-align: center;
        }

        .inner {
        background: rgba(255, 255, 255, 0.7);
        padding: 20px;
        }

        .frame {
            border-image:  url("data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAFQAAABUCAYAAAAcaxDBAAACbElEQVR4Xu2bwZLCQAhE4/9/9O7FsnTU9HRoRlO+vTIQePQgptzLxl+UwCUajWAbQMMiAChAwwTC4VAoQMMEwuFQKEDDBMLhUChAwwTC4VAoQG0Cf4NHq4hag9ul9zgANMwVoL8OVClA2RU/5T/aVTxlL43BkvM1M7dg95lufAVM2d38HuKVnAH63BuAhpl0AFVXarSPOVRnohsvweBWUyLYagCqYQAdCK1uUEJUKPSuiR8H6irIvYLVGasAqfyV/+7IOeKsEqoCqfqrmlT+yh+g5owGqPl67usUOkpefTVUa063vRWgmk9HigNoeGUAKEDjL4g+utiXPkUPzKSlNyhRnBr6HXPb4QpQh9bEWYBOQHKOnA6o2ku/7cq35pOYoQANr00ABei599COseJ8KC29QYli1R6aeEYFIECT9F7EahVAQj2tCTbAbc03AXTplToAuBVg61J7Db60gAnAS/NBoVv2/10BegKgaqZ2NHHv5qsrHx2DK4pb+rbnwJoE0IkPovsjKNQEpo6fHqgqYMWYUZD3FFzKr+T8JmuAOu2cOAvQCUjOEYA6tA6sJWqsuA1Q59UaVPXfxaWKnWGtElTPcP3VeYCKrq3+BbRqCAodCFQV3g5UfXdXHXcLXB1vZuzdzqj5ZgW7HlaAqlcYoAMBgJoyRaEmMHdmuuGVgt0xpV4fKruVv5vcq+BKkVZC2/Mb9GrByl/ZrfwBum0AtSSjgX0dUFVfNGH1sE/bE1de1QBQRci0A9QEpo4DVBHC/p7Aihn6U/wBGm43QAEaJhAOh0IBGiYQDodCARomEA6HQgEaJhAOh0LDQP8B/zaYVZPdn1oAAAAASUVORK5CYII=") 28 /  28px / 0 round;
            border-width:  28px;
            border-style:  solid;
        }

        .timer span {
        font-weight: bold;
        }

        @media  screen and  (min-width: 600px)  {
        .timer {
            width: 500px;
        }
        }

        canvas {
        position: absolute;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        }


        @media (max-width: 700px) {
        .sitter {
            display: none;
        }
        }

        .sitter {
        position: fixed;
        bottom: 15px;
        font-family: monospace;
        font-size: 11px;
        font-weight: bold;
        text-transform: uppercase;
        }

        .watch {
        background: rgba(255, 255, 255, 0.6);
        padding: 10px 15px;
        border-radius: 22px;
        display: inline-block;
        margin-right: 5px;
        }

        .left {
        left: 15px;
        }

        .right {
        right: 15px;
        }


        .twitter {
            background: url("data:image/png;base64,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");
            width: 33px;
            height: 33px;
            display: inline-block;
            background-repeat: no-repeat;
            background-color: rgba(255, 255, 255, 0.7);
            border-radius: 50%;
            background-size: 13px 13px;
            background-position: center;
            vertical-align: top;
        }

        .yt {
        color: #c4302b;
        }
    </style>
    </head>
    <body>
    <canvas></canvas>
    <div class="timer frame">
        <div class="inner">You have been honoring the pug for <span class="seconds">0</span> seconds<br/>
        You are a <span class="grade">Assistant</span> of pug</div></div>

        <div class="sitter left">
        <div class="watch">
        watch me making this:
        <a
            class="yt"
            href="https://www.youtube.com/watch?v=Sj1vbbRA07g"
            target="_blank"
            >youtube</a
        >
        </div>
        <a
        class="twitter"
        href="https://twitter.com/intent/tweet?url=https%3A%2F%2Fpuginarug.com&via=twholman&text=Do%20you%20love%20the%20pug?"
        target="_blank"
        ></a>
        </div>
        <div class="sitter right">
        <div class="watch">
            A <a href="https://theuselessweb.com" target="_blank">Useless Web</a> Project
        </div>
        </div>
    <script src='https://d33wubrfki0l68.cloudfront.net/js/0df80da62367fbd925570f0f802fa2a24a7e9d1a/index.js'></script>
    </body>
    </html>

### Código desenvolvido

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

### Resultado obtido
    https://www.youtube.com/watch?v=Sj1vbbRA07g
    https://twitter.com/intent/tweet?url=https%3A%2F%2Fpuginarug.com&via=twholman&text=Do%20you%20love%20the%20pug?
    https://theuselessweb.com