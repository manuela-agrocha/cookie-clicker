#!/usr/bin/env python
# coding: utf-8

# In[5]:


import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import pandas as pd
options = Options()
options.add_argument('--headless')
servico = Service(ChromeDriverManager().install())

navegador = webdriver.Chrome(service = servico)
navegador.get('https://finance.yahoo.com/') #abre a página no Chrome
dados_acoes = []

wait = WebDriverWait(navegador, 5) #espera 5 segundos até o elemento aparecer
most_active = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a[title="Stocks: Most Actives"]')))
most_active.click()
sleep(5)

for i in range(4): #loop para clicar no botão Next
    page_content = navegador.page_source #navegador.page_source: fornece o conteúdo html da página
    site = BeautifulSoup(page_content, 'html.parser')
    acoes = site.findAll('tr', attrs = {'class': 'simpTblRow'})
    
    for acao in acoes: #loop para pegar todas as informações de uma página  
        acao_nome = acao.find('a', attrs = {'class': 'Fw(600)'})
        nome = acao_nome['title']
        print('Nome:', nome)

        acao_sigla = acao.find('fin-streamer', attrs = {'class': 'Fw(600)'})
        sigla = acao_sigla['data-symbol']
        print('Sigla:', sigla)

        acao_porcent = acao.find('fin-streamer', attrs = {'data-field': 'regularMarketChangePercent'})
        porcentagem = round(float(acao_porcent['value']), 2)
        print(f'Variação em porcentagem: {porcentagem} %')

        acao_nominal = acao.find('fin-streamer', attrs = {'class': 'Fw(600)'})
        variacao_nominal = round(float(acao_nominal['value']), 2)
        print(f'Variação nominal: {variacao_nominal}')

        acao_volume = acao.find('fin-streamer', attrs = {'data-field': 'regularMarketVolume'})
        volume = int(acao_volume['value'])
        print(f'Volume: {volume:,}')

        acao_valor = acao.find('fin-streamer', attrs = {'data-field': 'marketCap'})
        valor_mercado = int(acao_valor['value'])
        print(f'Valor de mercado: {valor_mercado:,}')
        
        print()
        sleep(2)
        dados_acoes.append([nome, sigla, porcentagem, variacao_nominal, volume, valor_mercado])

    sleep(2)
    next_button = navegador.find_element(By.XPATH, '//*[@id="scr-res-table"]/div[2]/button[3]')
    
    if (next_button):
        next_button.click()

navegador.quit()

dados = pd.DataFrame(dados_acoes, columns=['Nome', 'Sigla', 'Variação (%)', 'Variação nominal', 'Volume', 'Valor de mercado'])
dados.to_excel('dados_acoes.xlsx', index = False)

print('concluído')

