from django.shortcuts import render
from pytube import YouTube
import moviepy.editor as mp
import os


def home(request):
    return render(request, 'home.html', {})

def downloads_video(request):
    if request.method == "POST":
        try:
            link = request.POST.get('link')
            video = YouTube(link)
            stream = video.streams.get_lowest_resolution()
            downloads_path = os.path.expanduser("~/Downloads")
            file_name = stream.default_filename
            stream.download(output_path=downloads_path)
            os.path.join(downloads_path, file_name)
            return render(request, 'downloads/video.html', {'msg': 'Vídeo Baixado'})
        except:
            return render(request, 'downloads/video.html', {'msg': 'Não foi Possível baixa o Vídeo '})
    else:
        return render(request, 'downloads/video.html', {})

def downloads_music(request):
    if request.method == "POST":
        url = request.POST.get('url')
        if url:
            try:
                yt = YouTube(url)
                audio_stream = yt.streams.filter(only_audio=True).first()
                if audio_stream:
                    downloads_path = os.path.expanduser("~/Downloads")
                    file_path = audio_stream.download(output_path=downloads_path)
                    mp3_path = os.path.splitext(file_path)[0] + '.mp3'
                    with mp.AudioFileClip(file_path) as audio_clip:
                        audio_clip.write_audiofile(mp3_path)
                    os.remove(file_path)
                    return render(request, 'downloads/music.html', {'msg': 'Música baixada!'})
                else:
                    return render(request, 'downloads/music.html', {'msg': 'O vídeo não tem áudio!'})
            except Exception as e:
                return render(request, 'downloads/music.html', {'msg': 'Não foi possível baixar o áudio!'})
        else:
            return render(request, 'downloads/music.html', {'msg': 'Insira uma URL válida!'})
    else:
        return render(request, 'downloads/music.html', {})
