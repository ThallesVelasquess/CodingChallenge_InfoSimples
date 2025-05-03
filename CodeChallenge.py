"""
Nome: Thalles Augusto Moura Velasques
LinkedIn: https://www.linkedin.com/in/thallesvelasques/
Email: thallesvelasques.contato@gmail.com
GitHub: https://github.com/ThallesVelasquess

Observações sobre o desafio: O Desafio foi feito por inteiro através do python interativo (arquivo de .ipynb), e a entrega final optei por passar o código para esse arquivo .py . No meu GitHub, Também está disponibilizado o arquivo .ipynb, que esta indicado como 'testes.ipynb' 
"""

# Bibliotecas que devem ser instaladas manualmente
from bs4 import BeautifulSoup
import requests

# Biblioteca nativa do sistema
import json

# Pegando a url do site
url = "https://infosimples.com/vagas/desafio/commercia/product.html"

# Atribuindo a url ao objeto 'response'
response = requests.get(url)

# Parse do responses
parsed_html = BeautifulSoup(response.content, "html.parser")

title = {}
# Seleciona o texto da tag 'h2' com id 'product_title'
title["title"] = parsed_html.select_one("h2#product_title").get_text()

brand = {}
# Seleciona o texto da tag 'div' que tem class='brand'
brand["brand"] = parsed_html.select_one("div.brand").get_text()

# Criação do objeto 'link', que armazena todo o conteúdo de caminho: tag 'div' que tem class='container' que contém uma 'nav' que logo
# busca todas as tags 'a'
links = parsed_html.select_one("div.container").find("nav").find_all("a")

# Criação de uma lista vazia para armazenar o texto de cada link
categories = []

# Laço for que armazena o texto de cada link a cada vez que roda
for link in links:
    categories.append(link.get_text())

# Criando um array de strings para 'categories'
c = {}
c["categories"] = categories

description = {}
# Seleciona o primeiro texto de caminho: tag 'div' que tem class='proddet' e tag 'p'
parsed_html.select_one("div.proddet").find_all("p")[0].get_text()

# Criação e armazenamento do texto de cada parágrafo em dois objetos diferentes
# Também é atribuído o .strip() para tirar espaçamentos que tem antes e depois de cada texto
texto_desc1 = parsed_html.select_one("div.proddet").find_all("p")[0].get_text().strip()
texto_desc2 = parsed_html.select_one("div.proddet").find_all("p")[1].get_text().strip()

# Criando a variavel que devolve o texto de cada parágrafo, acrecentando um espaço entre eles
description = texto_desc1 + " " + texto_desc2

# Selecionando a tag 'div' com class 'card-container' 
parsed_html.select("div.card-container")

# Selecionando o texto do primeiro elemento da tag 'div' com class 'prod-nome', ja eliminando os espaços com .strip()
parsed_html.select("div.prod-nome")[0].get_text().strip()

# Criação da lista 'skus'
skus = []

# Para cada nome no campo selecionado, pegar o texto dele e adicionar no campo 'nome' da lista 'skus' 
for name in parsed_html.select("div.prod-nome"):
    skus.append({
        "name": name.get_text().strip()
    })

# Selecionando o texto do segundo elemento da tag 'div' com class 'prod-pnow', ja eliminando os espaços com .strip()
parsed_html.select("div.prod-pnow")[1].get_text().strip()

# Criação da lista 'price_now'
price_now = []

# Laço for que roda para cada 'container' pertencente a tag 'div' com class 'card-container'
for container in parsed_html.select("div.card-container"):
    
    # Criação da variavel 'pnow_element' que armazena o conteudo da tag 'div' com class 'prod-pnow'
    pnow_element = container.select_one('div.prod-pnow')
    
    if pnow_element:
        # Remove "R$", espaços, substitui vírgula por ponto e converte para float
        preco_float = float(pnow_element.get_text().strip()
                            .replace('R$', '')
                            .replace(',', '.'))
    else:
        preco_float = None
    
    # Incrementa na lista criada 'price_now' a variavel 'preco_float'
    price_now.append({
        "preço": preco_float
    })

# Laço for que itera sobre 'skus' e 'price_now' simultaneamente para adicionar preços atuais
for i in range(len(skus)):
    # Adiciona o preço atual (price_now[i]["preço"]) ao dicionário do produto (skus[i])
    skus[i]["current_price"] = price_now[i]["preço"]

# Criação da lista 'price_old'
price_old = []

# Laço for que roda para cada 'container' pertencente a tag 'div' com class 'card-container'
for container in parsed_html.select("div.card-container"):
    
    # Criação da variavel 'pold_element' que armazena o conteudo da tag 'div' com class 'prod-pold'
    pold_element = container.select_one('div.prod-pold')
    
    if pold_element:
        # Remove "R$", espaços, substitui vírgula por ponto e converte para float
        preco_float = float(pold_element.get_text().strip()
                            .replace('R$', '')
                            .replace(',', '.'))
    else:
        preco_float = None
    
    # Incrementa na lista criada 'price_old' a variavel 'preco_float'
    price_old.append({
        "preço": preco_float
    })

# Laço for que itera sobre 'skus' e 'price_old' simultaneamente para adicionar preços atuais
for i in range(len(skus)):
    # Adiciona o preço atual (price_old[i]["preço"]) ao dicionário do produto (skus[i])
    skus[i]["old_price"] = price_old[i]["preço"]

# Criação da lista 'produtos'
produtos = []

# Laço for que roda para cada 'container' pertencente a tag 'div' com class 'card-container'
for container in parsed_html.select("div.card-container"):
    
    # Variavel que armazenará valor caso tenha, senão armazena 'None'
    indisponivel = container.find('i', string='Out of stock') is not None
    
    # Atribuindo 0 para caso esteja indisponivel, e 1 para caso disponivel
    status = 0 if indisponivel else 1
    
    # Incrementando na lista o 'status' atribuido ao campo de 'disponivel'
    produtos.append({
        "disponivel": status
    })

# Laço for que itera sobre 'skus' e 'produtos' simultaneamente para adicionar preços atuais
for i in range(len(skus)):
    # Adiciona o status (produtos[i]["disponivel"]) ao dicionário do produto (skus[i])
    skus[i]["available"] = produtos[i]["disponivel"]

# Selecionando os dados necessarios para o campo 'properties'
parsed_html.select("table.pure-table")[0]

# Selecionando todas as tags 'b'
parsed_html.select("table.pure-table")[0].find_all("b")

labels = []

# Laço for que coleta o texto das tags 'b' e incrementa na lista 'labels'
for label in parsed_html.select("table.pure-table")[0].find_all("b"):
    labels.append(label.get_text())

# Selecionando todas as tags 'td', começando pela segunda busca, e pulando de 2 em 2, sendo que as tags 'td' de indice par não
# seriam nescessárias
parsed_html.select("table.pure-table")[0].find_all("td")[1::2]

values = []

# Laço for que coleta o texto das tags 'td' e incrementa na lista 'values'
for value in parsed_html.select("table.pure-table")[0].find_all("td")[1::2]:
    values.append(value.get_text())

properties = []

# Para cada nome no campo selecionado, pegar o texto dele e adicionar no campo 'label' da lista 'properties' 
for label in labels:
    properties.append({
        "label": label
    })

# Laço for que itera sobre 'properties' e 'values' simultaneamente para adicionar preços atuais
for i in range(len(properties)):
    # Adiciona o status (values[i]) ao dicionário do produto (properties[i])
    properties[i]["value"] = values[i]

# Selecionando os dados necessarios para o campo 'reviews'
parsed_html.select(".pure-u-21-24")

# Selecionando os dados de class='analiseusername'
parsed_html.select(".analiseusername")

names = []

# Laço for que coleta o texto da class='analiseusername' e incrementa na lista 'names'
for name in parsed_html.select(".analiseusername"):
    names.append(name.get_text())

# Selecionando os dados de class='analisedate'
parsed_html.select(".analisedate")

dates = []

# Laço for que coleta o texto da class='analisedate' e incrementa na lista 'dates'
for date in parsed_html.select(".analisedate"):
    dates.append(date.get_text())

# Selecionando os dados de class='analisestars'
parsed_html.select(".analisestars")

stars_simbolo = []

# Laço for que coleta o texto da class='analisestars' e incrementa na lista 'stars_simbolo'
for star in parsed_html.select(".analisestars"):
    stars_simbolo.append(star.get_text())

# Converte cada avaliação em estrelas (ex: '★★★★☆') para um número inteiro  
# que representa a quantidade de estrelas preenchidas ('★')
stars = [int(avaliacao.count('★')) for avaliacao in stars_simbolo]
stars

# Selecionando os dados de class='analisebox' seguido pela tag 'p'
parsed_html.select(".analisebox p")

texts = []

# Laço for que coleta o texto da class='analisebox' seguido pela tag 'p' e incrementa na lista 'texts'
for text in parsed_html.select(".analisebox p"):
    texts.append(text.get_text())

reviews = []

# Laço for que coleta cada texto da lista 'names' e incrementa na lista 'reviews'
for name in names:
    reviews.append({
        "name": name
    })

for i in range(len(reviews)):
    # Adiciona o data (dates[i]) ao dicionário da review (reviews[i])
    reviews[i]["date"] = dates[i]

for i in range(len(reviews)):
    # Adiciona o score (stars[i]) ao dicionário da review (reviews[i])
    reviews[i]["score"] = stars[i]

for i in range(len(reviews)):
    # Adiciona o text (texts[i]) ao dicionário da review (reviews[i])
    reviews[i]["text"] = texts[i]

parsed_html.select_one("#comments h4").get_text()

# Atribuindo o texto que contém o 'Average score' a um objeto
ava_scr = parsed_html.select_one("#comments h4").get_text()

# Extrai o valor float usando split() e atrivui a variavel 'reviews_average_score'
reviews_average_score = float(ava_scr.split(':')[1].split('/')[0].strip())

# Atribuindo ao objeto 'url' o endereço do desafio
url = "https://infosimples.com/vagas/desafio/commercia/product.html"

# Criando o objeto que conterá a resposta final
resposta_final = {}

# Atribuindo os objetos que contem as respostas de cada campo para a resposta final
resposta_final['title'] = parsed_html.select_one('h2#product_title').get_text()
resposta_final['brand'] = parsed_html.select_one("div.brand").get_text()
resposta_final['categories'] = categories
resposta_final['description'] = description
resposta_final['skus'] = skus
resposta_final['properties'] = properties
resposta_final['reviews'] = reviews
resposta_final['reviews_average_score'] = reviews_average_score
resposta_final['url'] = url
resposta_final

json_resposta_final = {}

# Gerando o JSON com ensure_ascii=False, codificação UTF-8 e indent=4 para melhorar a visualização do arquivo json 
with open("produto.json", "w", encoding='utf-8') as arquivo_json:
    json.dump(resposta_final, arquivo_json, ensure_ascii=False, indent=4)

print("Arquivo JSON gerado com sucesso!")