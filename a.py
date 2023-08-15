from pytube import YouTube

# URL do vídeo do YouTube
video_url = "https://www.youtube.com/watch?v=tsmPCi7NKrg" 

# Crie uma instância do objeto YouTube
yt = YouTube(video_url)

# Obtenha a melhor stream de áudio disponível
audio_stream = yt.streams.filter(only_audio=True).first()

# Faça o download do arquivo de áudio
audio_stream.download(output_path=r"C:\Users\Prange\Downloads")

print('Download de áudio concluído.')











