from flask import Flask, request, render_template, jsonify, send_file
import os
import shutil
import requests

app = Flask(__name__)

@app.after_request
def add_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/player')
def player():
    artist = request.args.get('artist')
    song = request.args.get('song')
    #shutil.copyfile('separated\\htdemucs_ft\\'+artist+' - '+song+'\\vocals.wav', 'static/vocals.wav')
    #shutil.copyfile('separated\\htdemucs_ft\\'+artist+' - '+song+'\\no_vocals.wav', 'static/no_vocals.wav')
    #shutil.copyfile('lrc\\'+artist+' - '+song+'.lrc', 'static/output.lrc')
    return render_template('player.html', artist=artist, song=song)

@app.route('/list', methods=['GET'])
def get_list():
    return jsonify(os.listdir("separated/htdemucs_ft"))

@app.route('/get', methods=['GET'])
def get_content():
    artist = request.args.get('artist')
    song = request.args.get('song')
    
    download_data = requests.get('http://localhost:5000/download?artist='+artist+'&song='+song)
    song_path = download_data.json()["song_path"]
    print(song_path)
    separation_data = requests.get('http://localhost:5000/separate?path='+song_path)
    paths = separation_data.json()
    print(paths)
    generation_data = requests.get('http://localhost:5001/generate?path='+paths["vocals_path"]+'&artist='+artist+'&song='+song)
    lyric_data = generation_data.json()
    print(lyric_data)
    return render_template('player.html', artist=artist, song=song)

@app.route('/play', methods=['GET'])
def get_finished_audio_path():
    artist = request.args.get('artist')
    song = request.args.get('song')
    type = request.args.get('type')
    response = send_file('separated\\htdemucs_ft\\'+artist+' - '+song+'\\'+type+'.wav', as_attachment=False)
    response.headers['Content-Length'] = os.path.getsize('separated\\htdemucs_ft\\'+artist+' - '+song+'\\'+type+'.wav')
    response.headers['Content-Type'] = 'audio/wav'
    return response

@app.route('/lyrics', methods=['GET'])
def get_lyrics():
    artist = request.args.get('artist')
    song = request.args.get('song')
    return send_file('lrc\\'+artist+' - '+song+'.lrc', as_attachment=False)


if __name__ == '__main__':
    app.run(port=5002, debug=True)