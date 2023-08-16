from telegram.ext import Updater, CommandHandler
import telebot
import pandas as pd
from bs4 import BeautifulSoup as bs
import pandas as pd
from unidecode import unidecode
from tabulate import tabulate
import difflib
import time
from datetime import datetime
import scrapping_programacao as sp
import os


file_path = os.path.join(os.getcwd(), 'Last_modification.txt')

with open(file_path, 'r') as f:
    if f.read() != str(datetime.today().date()):
        print('Base de dados desatualizada.')
        print('Atualizando:')
        sp.macro()


def encontrar_string_proxima(string_procurada, df_column, grau_proximidade=0.6):
    lista_strings = df_column.str.split().explode().apply(
        lambda word: unidecode(word).lower())
    lista_strings = set(lista_strings.tolist())
    matches = difflib.get_close_matches(unidecode(
        string_procurada.lower()), lista_strings, n=3, cutoff=grau_proximidade)
    if matches:
        return matches


def column_to_tag(column):
    orig = [' ', '-', ',', '/']
    new = ['_', '_', '', '_']
    for o, n in zip(orig, new):
        column = column.str.replace(o, n)
    column = column.apply(lambda m: '/' + unidecode(m))
    return column


def format_table(DF):
    tablefmt = 'simple'       # Usar um formato de grade para exibir as linhas horizontais
    headers = 'keys'        # Exibir cabeçalhos
    showindex = False       # Não exibir o índice das linhas
    # Alinhar a primeira coluna à esquerda, as outras à direita
    colalign = ['left', 'right']
    numalign = 'right'      # Alinhar números à direita
    stralign = 'left'       # Alinhar strings à esquerda
    # Gerar a tabela formatada
    table = tabulate(DF, headers=headers, showindex=showindex, colalign=colalign,
                     numalign=numalign, stralign=stralign, tablefmt=tablefmt)
    return table


id = '1790463787'
file_path = file_path = os.path.join(os.getcwd(), 'teste.xlsx')

A = pd.read_excel(file_path, index_col=0)
bot = telebot.TeleBot('6507938494:AAHABkuPOSweeatRqan2Iag19OHoHJseKQU')

A['Programa'][A['Canal'] == 'SporTV 2'].unique()

A['Canal_tag'] = column_to_tag(A['Canal'])
A['Dia_tag'] = column_to_tag(A['Dia'])

filtro_canal = filtro_dia = ''


@bot.message_handler(commands=['cronograma_canal'])
def cronograma_canal(message):
    canais = A['Canal_tag'].unique()
    msg = ''
    for c in canais:
        msg += c+'\n'
    bot.send_message(
        message.chat.id, 'clique em qual canal gostaria de saber a programação:\n'+msg)


def check_canal(message):
    canais = A['Canal_tag'].unique()
    if message.text in canais:
        globals()['filtro_canal'] = message.text
        return True


@bot.message_handler(func=check_canal)
def cronograma_canal_select(message):

    msg = 'Ok, agora escolha qual dia você gostaria de saber a programação:'
    bot.send_message(message.chat.id, msg)

    dias = A['Dia_tag'].unique()
    msg = ''
    for d in dias:
        msg += d+'\n'

    bot.send_message(message.chat.id, msg)


def check_dia(message):
    dias = A['Dia_tag'].unique()
    if message.text in dias:
        globals()['filtro_dia'] = message.text
        return True


@bot.message_handler(func=check_dia)
def cronograma_canal_dia_select(message):
    print(filtro_canal, filtro_dia)

    msg = f"""Ótimo, já vou te buscar as correspondencias do canal {filtro_canal} no dia {filtro_dia} """
    bot.send_message(message.chat.id, msg)
    a = A[(A['Canal_tag'] == filtro_canal) & (
        A['Dia_tag'] == filtro_dia)]
    a = a.drop(['Categoria', 'Canal_tag', 'Dia_tag','Dia','Canal'], axis=1)
    p = 15
    print(len(a))
    time.sleep(2)
    for i in range(0, len(a), p):
        table = format_table(a[i:i+p])
        bot.send_message(message.chat.id, table)
        time.sleep(2)


# Resto
@bot.message_handler(commands=['cronograma_programa'])
def tendi_nao(message):
    msg = """Perfeito, vamos lá !!!\n
Existem muitas maneiras de utilizar essa funcinalidade mas vamos começar por algo simples, como buscar por parte do nome do programa.\n
Exemplo, digite "programa=Corinthians", "programa=tenis feminino duplas" ou então "programa=Volei Brasil Masculino"\n
"""
    bot.send_message(message.chat.id, msg)


def check(message):
    m = message.text.lower()
    if 'programa' in m and '=' in m:
        return True


def filtro_programa(A, filtros):
    A['Programa'] = A['Programa'].str.replace(
        ':', '').apply(lambda m: unidecode(m))

    filtro = True
    for p in filtros.strip().split(' '):
        filtro &= A['Programa'].str.contains(unidecode(p), case=False)

    return A[filtro]


@bot.message_handler(func=check)
def busca_cronograma(message):
    n = message.text.split("=")[-1].strip()
    msg = f"""Ótimo, já vou te buscar as correspondencias de "{n}" """
    bot.send_message(message.chat.id, msg)
    a = filtro_programa(A, n)
    a = a.drop(['Categoria', 'Canal_tag', 'Dia_tag'], axis=1)
    p = 15

    if len(a) > 0:
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


# Resto
@bot.message_handler(func=lambda m: True)
def geral(message):
    f_name=message.from_user.first_name
    msg = f"""Perfeito, vamos lá {f_name} !!!
Se deseja saber a programação de um programa específico digite /cronograma_programa
Se deseja saber o cronograma de um canal específico digite /cronograma_canal
"""
    bot.send_message(message.chat.id, msg)


print('Tudo Perfeito ! Rodando !')
bot.polling()
