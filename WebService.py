import time
from flask import Flask, request, render_template, jsonify, send_file
from Pipeline import Pipeline

import threading
import os

app = Flask(__name__)
pipeline = Pipeline()

@app.after_request
def add_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/downloads')
def downloads():
    return render_template('downloads.html')

@app.route('/player')
def player():
    artist = request.args.get('artist')
    song = request.args.get('song')
    return render_template('player.html', artist=artist, song=song)

@app.route('/list', methods=['GET'])
def get_list():
    return jsonify(os.listdir("separated/htdemucs_ft"))

@app.route('/queue')
def get_queue():
    return jsonify(pipeline.get_queue())

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

@app.route('/get', methods=['GET'])
def get_content():
    artist = request.args.get('artist')
    song = request.args.get('song')
    
    pipeline.add_song(artist, song)
    return render_template('player.html', artist=artist, song=song)

def run_pipeline():
    while(True):
        time.sleep(2)
        pipeline.add_task()

if __name__ == '__main__':
    pipeline_thread = threading.Thread(target=run_pipeline)
    pipeline_thread.start()
    app.run(port=5002, debug=True, use_reloader=False)