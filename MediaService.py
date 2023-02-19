from __future__ import unicode_literals
from googleapiclient.discovery import build
from flask import Flask, request, jsonify
#from demucs import separate
from demucs.separate import main
from dotenv import dotenv_values
import yt_dlp

class MediaService:

    def __init__(self, key, path, format, codec, quality, project_dir='C:\\Users\\Njose\\Documents\\Projects\\karaoke\\'):
        self.project_dir = project_dir
        self.youtube_key = key
        self.path = path
        self.options = {
            'outtmpl': path + '/%(title)s.%(ext)s',
            'format': format,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': codec,
                'preferredquality': str(quality),
            }],
            'logger': MyLogger(),
            'progress_hooks': [self.progress_hook],
        }

    def search_youtube(self, query, num):
        api_key = self.youtube_key
        youtube = build('youtube', 'v3', developerKey=api_key)

        request = youtube.search().list(
            part='id',
            q=query,
            type='video',
            maxResults=num,
            order='relevance'
        )

        response = request.execute()

        video_ids = [item['id']['videoId'] for item in response['items']]
        video_links = ['https://www.youtube.com/watch?v=' + video_id for video_id in video_ids]

        return video_links

    def progress_hook(self, d):
        if d['status'] == 'downloading':
            progress = d['_percent_str']
            speed = d['_speed_str']
            eta = d['_eta_str']
            print(f'Progress: {progress}, Speed: {speed}, ETA: {eta}')
        elif d['status'] == 'finished':
            print('Download finished')
        elif d['status'] == 'error':
            print('Error during download')

    def query(self, artist, song):
        return "{} - {} (Audio)".format(artist, song)

    def download(self, artist, song):
        self.options['outtmpl'] = self.path + '/'+artist+' - '+song+'.%(ext)s'
        search = self.query(artist, song)
        with yt_dlp.YoutubeDL(self.options) as ydl:
            ydl.download(self.search_youtube(search, 1))

        return self.path+'/'+artist+' - '+song+'.mp3'

    def separate(self, path):
        args = [self.project_dir+path, "--two-stems=vocals", "-n", "htdemucs_ft"]
        parser = main(args)

        return 'separated\\htdemucs_ft'+path.replace(self.path, '')[:-4]+'/'

class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)

app = Flask(__name__)
config = dotenv_values(".env")
ms = MediaService(config["youtube_key"], config["path"], config["format"], config["codec"], config["quality"])

@app.route('/download', methods=['GET'])
def download():
    artist = request.args.get('artist')
    song = request.args.get('song')
    print("Started download for "+song+" by "+artist)
    song_path = ms.download(artist, song)
    print("Finished download for "+song+" by "+artist)
    return jsonify({
        "song_path": song_path
    })

@app.route('/separate', methods=['GET'])
def separate():
    song_path = request.args.get('path')
    print("Started separation at "+song_path)
    separate_path = ms.separate(song_path)
    print("Finished separation at "+song_path)
    return jsonify({
        "vocals_path": separate_path + 'vocals.wav',
        "background_path": separate_path + 'no_vocals.wav'
    })


if __name__ == '__main__':
    app.run(port=5000, debug=True)