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
import os
from pytube import YouTube

import scrapping_programacao as sp
from last import get_top_tracks


tracks=''
filtro_musicas=''
filtro_banda=''

id = '1790463787'
file_path = file_path = os.path.join(os.getcwd(), 'teste.xlsx')

A = pd.read_excel(file_path, index_col=0)
bot = telebot.TeleBot('6507938494:AAHABkuPOSweeatRqan2Iag19OHoHJseKQU')



def check_musica(message):
    if message.text in filtro_musicas:
        return True

@bot.message_handler(func=check_musica)
def download_musica(message):

    b = tracks[tracks['name_tag']==message.text]


    nome = b.iloc[0]['name']
    url = b.iloc[0]['url']

    print(nome,url)

    yt = YouTube(url)
    video = yt.streams.filter(only_audio=True).first()
    video.download(output_path=f'Musicas',filename=nome+'.mp3')
    msg='Musica baixada, aguarde enquanto faço o upload...'
    bot.send_message(message.chat.id, msg)
    bot.send_audio(message.chat.id,audio=open(f'Musicas\{nome}.mp3','rb'))


def check_banda(message):
    m = message.text.lower()
    if 'banda' in m and '=' in m:
        return True
    
@bot.message_handler(func=check_banda)
def download_banda(message):
    n = message.text.split("=")[-1].strip()
    nome_banda,top_tracks=get_top_tracks(n)
    msg = f"""Ótimo, já vou te buscar as correspondencias de "{nome_banda}" """
    bot.send_message(message.chat.id, msg)
    
    print(message.from_user.first_name)
    print(n)
    B=pd.DataFrame(top_tracks,columns=('name','url'))
    B['name_tag']=column_to_tag(B['name'])

    globals() ['tracks'] = B
    globals() ['filtro_musicas'] = tracks['name_tag'].unique()
    msg = ''
    for b in B['name_tag']:
        msg += b+'\n'
    bot.send_message(
        message.chat.id, 'clique em qual musica gostaria de fazer o download:\n'+msg)


@bot.message_handler(commands=['download_banda'])
def download_banda(message):
    msg = '''Perfeito, vou te passar uma lista das 15 músicas mais populares de uma banda, para que você possa escolher qual delas deseja baixar. 
Para isso, digite o nome da banda no formato a seguir, como por exemplo: 'banda=ACDC'
'''
    bot.send_message(message.chat.id, msg)






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
    orig = ["""['")(.,]""",
            """[ -/]"""]
    new = ['',
           '_']
    for o, n in zip(orig, new):
        column = column.str.replace(o, n,regex=True)
    column = column.apply(lambda m: '/' + unidecode(m))
    return column


A['Programa'][A['Canal'] == 'SporTV 2'].unique()
A['Canal_tag'] = column_to_tag(A['Canal'])
A['Dia_tag'] = column_to_tag(A['Dia'])

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



filtro_canal = filtro_dia = ''


@bot.message_handler(commands=['busca_por_canal'])
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

    msg = f"""Ótimo, já vou te buscar as correspondencias do canal {filtro_canal} no dia {filtro_dia} """
    bot.send_message(message.chat.id, msg)
    a = A[(A['Canal_tag'] == filtro_canal) & (
        A['Dia_tag'] == filtro_dia)]
    a = a.drop(['Categoria', 'Canal_tag', 'Dia_tag','Dia','Canal'], axis=1)
    p = 15
    print(message.from_user.first_name)
    print(filtro_canal, filtro_dia)
    print(len(a))
    time.sleep(2)
    for i in range(0, len(a), p):
        table = format_table(a[i:i+p])
        bot.send_message(message.chat.id, table)
        time.sleep(2)
    


# Resto
@bot.message_handler(commands=['busca_por_nome'])
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

    print(message.from_user.first_name)
    print(n)
    print(len(a))

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
#     msg = f"""Perfeito, vamos lá {f_name} !!!
# 1) Se deseja saber a programação de um programa específico clique em /cronograma_programa
# 2) Se deseja saber o cronograma de um canal específico clique em /cronograma_canal
# 3) Se deseja baixar algumas musicas de uma banda clique em /download_banda
# """

    msg="""Perfeito, vamos lá Nathália !!!

Programação de canais de esportes:

1) Se deseja saber a programação de um canal específico clique em /busca_por_canal

2) Se deseja fazer a busca livre pelo nome do programa clique em /busca_por_nome

————————————————-

Músicas:

Se deseja baixar algumas musicas de uma banda clique em /download_banda"""

    bot.send_message(message.chat.id, msg)


print('Tudo Perfeito ! Rodando !')
bot.polling()
