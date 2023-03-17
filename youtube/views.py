from django.shortcuts import render
from pytube import YouTube
import moviepy.editor as mp
import os
import re


def home(request):
    return render(request, 'home.html', {})

def downloads_video(request):
    if request.method == "POST":
        try:
            link = request.POST['link']
            video = YouTube(link)
            print(1)
            stream = video.streams.get_lowest_resolution()
            #stream = video.streams.get_by_itag(22)
            #stream = video.streams.filter('resolution').first()
            #stream = video.streams.get_by_resolution("144p")
            #stream = video.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
            print(1)
            stream.download()
            print(1)
            return render(request, 'downloads/video.html', {'msg': 'Vídeo Baixado'})
        except:
            return render(request, 'downloads/video.html', {'msg': 'Não foi Possivel baixa o Vídeo '})
    else:
        return render(request, 'downloads/video.html', {})
    
def downloads_music(request):
    if request.method == "POST":
        url = request.POST.get('url')
        if url:
            try:
                yt = YouTube(url)
                print(1)
                audio_stream = yt.streams.filter(only_audio=True).first()
                #audio_stream = yt.streams.get_audio_only()
                print(1)
                if audio_stream:
                    audio_path = audio_stream.download()
                    for file in os.listdir(audio_path):
                        if re.search('mp4', file):
                            mp4_path = os.path.join(audio_path, file)
                            mp3_path = os.path.join(audio_path, os.path.splitext(file)[0] + '.mp3')
                            audio_clip = mp.AudioFileClip(mp4_path)
                            audio_clip.write_audiofile(mp3_path)
                            os.remove(mp4_path)
                    return render(request, 'downloads/music.html', {'success': True})
                else:
                    return render(request, 'downloads/music.html', {'msg': 'O vídeo não tem audio!'})
            except Exception as ec:
                return render(request, 'downloads/music.html', {'msg': str(ec)})
        else:
            return render(request, 'downloads/music.html', {'msg': 'Insira uma url Válida!'})
    else:
        return render(request, 'downloads/music.html', {})
