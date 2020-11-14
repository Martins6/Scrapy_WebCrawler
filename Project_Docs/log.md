# ~~Captain's~~ Project's Log

## 11/11

Pensei como deveria melhor realizar esse projeto e qual seria o tema das notícias que faria raspagem. Resumidamente, cheguei a conclusão que o melhor jeito seria utilizando algum framework em Python para a raspagem de dados e utilizar algum BD para armazenar as informações extraídas e geradas. Provavél que eu faça em MySQL pela sua popularidade, embora só tenha experiência prática em PostgreSQL.

Uma observação importante que constatei é que muitos sites de noticías requerem uma conta registrada ou subscripção no site. Irei evitar esses site para que aquele que testar da Oncase não precise registrar uma conta ou pagar uma subscripção.

Falta decidir o tema dos sites e o exato framework do Web Crawler.

## 12/11

Optei por 3 sites de notícias famosos no Brasil: BBC Brasil, CNN Brasil e Globo (G1).

Também decidir usar o framework Scrapy (talvez com o parser de html Beautifulsoup), sendo uma biblioteca pura em Python. Estou utilizando também o SelectorGadjet (o qual já estava instalado em meu browser) para poder auxiliar na pesquisa dos elementos em CSS ou HTML.

Revisei e aprendi novas técnicas utilizando o Scrapy através da documentação da biblioteca.

Tentei aplicar no site do G1, porém percebi que algumas variáveis dentro de cada artigo de jornal poderia ser nova. Não há um objeto em comum no corpo do texto. Deixarei em off, por enquanto.

Comecei a criar a Spider da CNN, porém não consegui terminar hoje.

## 13/11

Terminei a spider da CNN, consegui retirar os dados requisitado das páginas.

Percebi que li errado as requisições do projeto pois o documento especifica dizendo: "dados de portais concorrentes em uma _área específica_ (ex.: games, tech, carros)", eu não posso utilizar os sites da BBC, CNN, etc.. Irei salvar a Spider da CNN para projetos futuros.

Pensei novamente e escolhi sites de notícias da cultura Geek. São estes os três (com hyperlink):

1. [Jornada Geek](https://www.jornadageek.com.br/novidades/)
2. [Jovem Nerd](https://jovemnerd.com.br/)
3. [TecMundo](https://www.tecmundo.com.br/cultura-geek) 

Terminei a construção da Spider do Jornada Geek, faltando apenas a formatação de datas.

## 14/11