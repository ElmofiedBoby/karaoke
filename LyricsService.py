from flask import Flask, request, jsonify
import whisper

app = Flask(__name__)
model = whisper.load_model("small")

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
