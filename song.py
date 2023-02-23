from taskstate import TaskState
import dramatiq

# Define a task object that includes a command and its arguments
class Song:

    def __init__(self, artist, song, ms, model, state=TaskState.QUEUED):
        self.artist = artist
        self.song = song
        self.state = state
        self.ms = ms
        self.model = model
        
        self.download_path = None
        self.vocals_path = None
        self.lyrics = None
    
    #@dramatiq.actor(max_retries=3)
    def download(self):
        self.state = TaskState.DOWNLOADING
        print(f'{self.artist} - {self.song}: {self.state}')
        download_path = self.ms.download(self.artist, self.song)
        self.state = TaskState.DOWNLOADED
        print(f'{self.artist} - {self.song}: {self.state}')
        return download_path

    #@dramatiq.actor(max_retries=3)
    def separate(self, download_path):
        self.state = TaskState.SEPARATING
        print(f'{self.artist} - {self.song}: {self.state}')
        vocals_path = self.ms.separate(download_path) + 'vocals.wav'
        self.state = TaskState.SEPARATED
        print(f'{self.artist} - {self.song}: {self.state}')
        return vocals_path

    #@dramatiq.actor(max_retries=3)
    def transcribe(self, vocals_path):
        self.state = TaskState.TRANSCRIBING
        print(f'{self.artist} - {self.song}: {self.state}')
        result = self.model.transcribe(vocals_path)
        segments = result['segments']
        lyrics = self.ms.convert_lyrics(segments, self.artist, self.song)
        self.state = TaskState.TRANSCRIBED
        print(f'{self.artist} - {self.song}: {self.state}')
        return lyrics