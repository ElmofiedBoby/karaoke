from __future__ import unicode_literals
from googleapiclient.discovery import build
from flask import Flask, request, jsonify
from demucs.separate import main
from dotenv import dotenv_values
import yt_dlp
import whisper

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

def convert_lyrics(segments, artist, song):
    openai_output = segments
    lrc_output = ""
    for segment in openai_output:
        start_time = int(segment["start"])
        end_time = int(segment["end"])
        text = segment["text"]
        lrc_output += f"[{start_time:02}:{int((start_time % 1) * 100):02}]"
        lrc_output += f"[{end_time:02}:{int((end_time % 1) * 100):02}]"
        lrc_output += text + "\n"
    
    with open('lrc/'+artist+' - '+song+'.lrc', 'w', encoding='utf-8') as f:
        f.write(lrc_output)
    return jsonify({
        'lrc_output': lrc_output,
        'saved_path': 'lrc/'+artist+' - '+song+'.lrc'
    })

app = Flask(__name__)
model = whisper.load_model("small")
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

@app.route('/generate', methods=['GET'])
def generate_lyrics():
    path = request.args.get('path')
    artist = request.args.get('artist')
    song = request.args.get('song')
    print("Started transciption from: "+path)
    result = model.transcribe(path)
    print("Finished transcription from: "+path)
    segments = result['segments']
    print("Started LRC conversion from: "+path)
    lyrics = convert_lyrics(segments, artist, song)
    print("Finished LRC conversion from: "+path)
    return lyrics


if __name__ == '__main__':
    app.run(port=5001, debug=True)