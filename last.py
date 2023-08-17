import requests
from bs4 import BeautifulSoup as bs
from pytube import YouTube


def get_top_tracks(banda, n=15):
    """ Retorna o nome da banda e uma lista de touples das top tracks e seus urls do youtube
    """
    query = banda

    base_url = "https://www.google.com/search"
    params = {
        # "q": 'last.fm/music ' + query
        "q": 'last.fm ' + query
    }

    req = requests.get(base_url, params=params)
    soup = bs(req.text, "html.parser")
    req.url

    f1e = soup.select(
        'a[href*="https://www.last.fm/"]')[0]['href'].split('&sa')[0].split('q=')[1]
    url = f1e+'/+tracks?date_preset=ALL#top-tracks'

    req = requests.get(url)
    soup = bs(req.text, "html.parser")

    nome_banda = soup.find('div', {'class', 'header-new-content'}).h1.text

    print(nome_banda)

    top_tracks = soup.find_all('tr', {'itemprop': 'track'})

    A = []
    for track in top_tracks[:n]:
        nome = track.find(
            'td', {'class': 'chartlist-name'}).text.replace('\n', '')
        url = track.find('td', {'class': 'chartlist-play'}).a['href']
        A.append((nome, url))

    return nome_banda, A

# print(nome)
# yt = YouTube(url)
# video = yt.streams.filter(only_audio=True).first()
# video.download(output_path=f'Musicas/{nome_banda}',filename=nome+'.mp3')
