# pip install youtube-dl pafy
import sys
import os
import pafy
import re

def download(url):
    if url.find("music") != -1:
        url = url.replace("music.", "")

    try:
        stream = pafy.new(url)
        menu(stream)
    except:
        print("Что-то пошло не так! Попробуйте еще раз...")

def menu(stream):
        print("Что-бы скачать видео введите: 1 | Что-бы скачать аудио введите: 2 ")
        choice = input("Введите цифру: ")
        if choice == "1":
            downloadVideo(stream)
        elif choice == "2":
            downloadMusic(stream)
        else:
            print("Не верно введено число!")
            replay = input("Повторить ввод (y/n): ")
            if replay == "y":
                menu(stream)
            else:
                print("Завершение!")
                sys.exit()

def downloadVideo(stream):
#    video_streams = stream.videostreams
    video_streams = stream.streams
    downloadStream(video_streams, "video")

def downloadMusic(stream):
    audio_streams = stream.audiostreams
    downloadStream(audio_streams, "audio")

def downloadStream(streams, type):

    available_streams = {}
    count = 1
    for media in streams:
        available_streams[count] = media

        if type == "video":
            print(f"{count}: {type} {media.resolution} {media.extension} размер: {round(media.get_filesize()/1000000, 1)} Мб")
        else:
            print(f"{count}: {type} {media.bitrate} {media.extension} размер: {round(media.get_filesize()/1000000, 1)} Мб")
        
        count += 1
    downloadFile(streams, type, count)

def downloadFile(streams, type, count):
    try:
        stream_count = int(input("Введите номер: "))
    except:
        stream_count = False
    if stream_count and stream_count < count:
        print("Загрузка...")
#        streams[stream_count - 1].download(filepath="/tmp/Game." + streams[stream_count - 1].extension)
        streams[stream_count - 1].download()
    else:
        print("Неверно выбрана цифра!")
        downloadStream(streams, type)

    ask = input("Конвертировать в mp3 (y/n): ")
    if ask == "y":
        downloadMp3(streams[stream_count - 1])

def downloadMp3(media):
    name = media.title + "." + media.extension
    os.rename(name, "dwl." + media.extension)
    os.system("ffmpeg\\ffmpeg -i dwl." + media.extension + " mp3\\" + rename(media.title) + ".mp3")
    os.remove("dwl." + media.extension)

def rename(name):
    try:
        name = name.replace(" ", "_")
    except:
        pass
    try:
        name = name.replace(",", "_")
    except:
        pass
    try:
        name = name.replace("&", "_and_")
    except:
        pass
    try:
        name = name.replace("-", "_")
    except:
        pass
    return name

if __name__ == "__main__":
    print("Хотите скачать видео или аудио с YouTube? Просто введите URL ниже...")
    url = input("Введите URL: ")

    if url.find("youtube") != -1:
        download(url)
    else:
        print("Неверный url...")