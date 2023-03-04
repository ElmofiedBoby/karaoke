import time
from flask import Flask, request, render_template, jsonify, send_file
from Pipeline import Pipeline
from task import TaskState

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
    return render_template('download.html')

@app.route('/player')
def player():
    artist = request.args.get('artist')
    song = request.args.get('song')
    return render_template('player.html', artist=artist, song=song)

@app.route('/list', methods=['GET'])
def get_list():
    state = request.args.get('state')
    data = []

    if state == 'finished':
        for item in pipeline.song_list:
            if item.state == TaskState.FINISHED:
                data.append(f"{item.artist} - {item.song}")
    elif state == 'notfinished':
        for item in pipeline.song_list:
            if item.state is not TaskState.FINISHED:
                data.append(f"{item.artist} - {item.song} - {item.state}")
    else:
        for item in pipeline.song_list:
            data.append(f"{item.artist} - {item.song} - {item.state}")
            
    return jsonify(data)

@app.route('/queue')
def get_queue():
    returnval = []
    pipeline_queue = pipeline.get_queue()
    while not pipeline_queue.empty():
        item = pipeline_queue.get_nowait()
        returnval.append({
            "artist": item.artist,
            "song": item.song,
            "state": item.state
        })
    
    print(returnval)
    return jsonify(returnval)

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
    
    pipeline.add_song(artist, song, TaskState.QUEUED)
    return render_template('download.html')

def run_pipeline():
    while(True):
        time.sleep(2)
        pipeline.run()

if __name__ == '__main__':
    pipeline_thread = threading.Thread(target=run_pipeline)
    pipeline_thread.start()
    app.run(port=5002, debug=True, use_reloader=False)