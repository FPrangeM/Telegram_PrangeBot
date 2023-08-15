import requests
from telegram.ext import Updater, CommandHandler
import telebot
import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
from unidecode import unidecode
import re
from tabulate import tabulate
import difflib
import time
from datetime import datetime
import scrapping_programacao as sp

sp.macro()

def remover_acentos(text):
    return unidecode(text)


def filtro_programa(A, filtros):
    A['Programa'] = A['Programa'].str.replace(':', '').apply(remover_acentos)

    filtro = True
    for p in filtros.strip().split(' '):
        filtro &= A['Programa'].str.contains(unidecode(p), case=False)

    return A[filtro]


def format_table(DF):
    tablefmt = 'simple'       # Usar um formato de grade para exibir as linhas horizontais
    headers = 'keys'        # Exibir cabeçalhos
    showindex = False       # Não exibir o índice das linhas
    # Alinhar a primeira coluna à esquerda, as outras à direita
    colalign = ['left', 'right', 'right']
    numalign = 'right'      # Alinhar números à direita
    stralign = 'left'       # Alinhar strings à esquerda
    # Gerar a tabela formatada
    table = tabulate(DF, headers=headers, showindex=showindex, colalign=colalign,
                     numalign=numalign, stralign=stralign, tablefmt=tablefmt)
    return table


def verify_string_presence(list_strings, string):
    result = [s.lower() in string.lower() for s in list_strings]
    if all(result):
        return True


A = pd.read_excel('teste.xlsx', index_col=0)


def encontrar_string_proxima(string_procurada, df_column, grau_proximidade=0.6):

    lista_strings = df_column.str.split().explode().apply(
        lambda word: unidecode(word).lower())
    lista_strings = set(lista_strings.tolist())

    matches = difflib.get_close_matches(unidecode(
        string_procurada.lower()), lista_strings, n=3, cutoff=grau_proximidade)

    if matches:
        return matches


bot = telebot.TeleBot('6507938494:AAHABkuPOSweeatRqan2Iag19OHoHJseKQU')


# Resto
@bot.message_handler(commands=['cronogramas'])
def tendi_nao(message):
    msg = """Perfeito, vamos lá !!!\n
Existem muitas maneiras de utilizar essa funcinalidade mas vamos começar por algo simples, como buscar por parte do nome do programa.\n
Exemplo, digite "programa=Corinthians", "programa=tenis feminino duplas" ou então "programa=Volei Brasil Masculino"\n
Se deseja saber de quais canais estou buscando, ou de qual intervalo de data, digite /cronograma_info"""
    bot.send_message(message.chat.id, msg)


# Resto
@bot.message_handler(commands=['cronograma_info'])
def tendi_nao(message):
    msg = """Ok, aqui vão as infos!!!"""
    bot.send_message(message.chat.id, msg)

    d1 = A['Dia'].iloc[0]
    d2 = A['Dia'].iloc[-1]
    msg = f"""A programação foi coletada entre os dias {d1} e {d2}."""
    bot.send_message(message.chat.id, msg)

    c = ','.join(list(A['Canal'].unique())).replace(',', '\n')
    msg = f"""Já os canais analizados foram os seguintes \n {c}"""
    bot.send_message(message.chat.id, msg)


@bot.message_handler(commands=['user'])
def data(message):
    global m
    m = message
    return None


def check(message):

    if verify_string_presence(['programa', '='], message.text):
        return True


@bot.message_handler(func=check)
def busca_cronograma(message):
    n = message.text.split("=")[-1].strip()
    msg = f"""Ótimo, já vou te buscar as correspondencias de "{n}" """
    bot.send_message(message.chat.id, msg)
    a = filtro_programa(A, n)
    a = a.drop('Categoria', axis=1)

    nome = message.from_user.first_name + ' ' + message.from_user.last_name
    conteudo = n
    retorno = str(len(a))

    reg = [nome, conteudo, retorno]

    with open('registros.txt', 'a') as f:
        for r in reg:
            f.write(r+'\n')
            print(r)
        f.write('\n')

    p = 10

    if len(a) > 0 and len(a) <= p:
        table = format_table(a)
        bot.send_message(message.chat.id, table)
    elif len(a) > p:
        msg = f'Vish, foram tantos resultados que só vou conseguir te mandar de {p} em {p}\nTalvez colocar mais palavras ajude a filtrar'
        bot.send_message(message.chat.id, msg)
        time.sleep(2)
        for i in range(0, len(a), p):
            table = format_table(a[i:i+p])
            bot.send_message(message.chat.id, table)
            time.sleep(2)

    else:
        msg = 'Vish, não teve nenhuma correspondencia pela sua pesquisa'
        bot.send_message(message.chat.id, msg)
        k = 0
        for i in n.split(' '):
            if encontrar_string_proxima(i, A['Programa']) != None:
                k = 1
        if k == 1:
            try:
                msg = 'Se você estava buscando outra coisa, sugiro testar o seguinte:'
                bot.send_message(message.chat.id, msg)

                msg = ''
                for i in n.split(' '):
                    msg += i+'-->  ' + \
                        ' ou '.join(
                            [k for k in encontrar_string_proxima(i, A['Programa'])])+'\n'
                bot.send_message(message.chat.id, msg)

            except:
                print('deun')

# n='curintcha'
# for i in n.split(' '):
#     print(encontrar_string_proxima(i, A['Programa']))
# encontrar_string_proxima('curintcha',A['Programa'])


@bot.message_handler(func=lambda m: True)
def tendi_nao(message):
    msg = """Fala Cumpadi, estou sendo melhorado aos poucos mas por hora já tenho uma funcionalidade para buscar a programação de vários canais de esporte \n
Porquê não testa ? Digite ou clique:\n /cronogramas """
    bot.send_message(message.chat.id, msg)


bot.polling()
