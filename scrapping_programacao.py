from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
from unidecode import unidecode


def programacao(url, canal):

    DF = pd.DataFrame(
        columns=['Programa', 'Categoria', 'Horario', 'Dia', 'Canal'])

    req = requests.get(url)
    soup = bs(req.content, 'html.parser')

    box = soup.find('ul', {'class': 'mw'})
    itens = box.find_all(['ul', {'class': 'mw'}, 'li', {
                         'class': 'subheader devicepadding'}])
    itens[1].h3

    programa, categoria, horario, dia = '', '', '', ''
    i = 1
    for item in itens:
        try:
            if item['class'] == ['subheader', 'devicepadding']:

                dia = item.text
            pass
        except:

            try:
                programa = item.h2.text
                categoria = item.h3.text
                horario = item.find('div', {'class': 'lileft time'}).text
                DF.loc[i] = programa, categoria, horario, dia, canal
                i += 1
            except:
                pass

    DF = DF[['Programa', 'Categoria', 'Dia', 'Horario', 'Canal']]
    return DF


def remover_acentos(text):
    return unidecode(text)


def filtro_programa(A, filtros):
    A['Programa'] = A['Programa'].apply(remover_acentos)

    filtro = True
    for p in filtros.split(' '):
        filtro &= A['Programa'].str.contains(p, case=False)

    return A[filtro]


def macro():
    DF = pd.DataFrame(
        columns=['Programa', 'Categoria', 'Horario', 'Dia', 'Canal'])

    url = 'https://meuguia.tv/programacao/categoria/Esportes'
    req = requests.get(url)
    soup = bs(req.content, 'html.parser')
    box = soup.find('ul')
    canais = box.find_all('a', {'class': 'devicepadding'})

    for c in canais:

        sufixo = c['href']
        url = 'https://meuguia.tv'+sufixo
        canal = c.h2.text
        print(canal)
        DF = pd.concat([DF, programacao(url, canal)],
                       axis=0, ignore_index=True)

    DF.to_excel('teste.xlsx')
    print('base atualizada')


if __name__ == '__main__':

    DF = pd.DataFrame(
        columns=['Programa', 'Categoria', 'Horario', 'Dia', 'Canal'])

    url = 'https://meuguia.tv/programacao/categoria/Esportes'
    req = requests.get(url)
    soup = bs(req.content, 'html.parser')
    box = soup.find('ul')
    canais = box.find_all('a', {'class': 'devicepadding'})

    for c in canais:

        sufixo = c['href']
        url = 'https://meuguia.tv'+sufixo
        canal = c.h2.text
        print(canal)
        DF = pd.concat([DF, programacao(url, canal)],
                       axis=0, ignore_index=True)

    DF.to_excel('teste.xlsx')
