from song import Song
from taskstate import TaskState
from dotenv import dotenv_values

import queue
import whisper
import json

from MediaService import MediaService

class Pipeline:

    def __init__(self):
        # Create an event queue
        self.song_queue = queue.Queue()
        self.model = whisper.load_model("small")
        config = dotenv_values(".env")
        self.ms = MediaService(config["youtube_key"], config["path"], config["format"], config["codec"], config["quality"])
        print("Initialized!")

    def add_song(self, artist, song, state):
        data = {
            'artist': artist,
            'song': song,
            'state': state.__json__()
        }
        #song = Song(artist, song, self.ms, self.model, state)
        print(f'{artist} - {song}: {state}')
        self.song_queue.put(json.dumps(data, indent = 4))

    def get_queue(self):
        return self.song_queue

    def add_task(self):

        try:
            # JSON representation
            request = self.song_queue.get()
            # DICT representation
            data = json.loads(request)
            # OBJECT REPRESENTATION
            song = Song(data["artist"], data["song"], self.ms, self.model, TaskState.fromJSON(data["state"]))

            if song.state == TaskState.QUEUED:
                song.download_path = song.download()
                self.add_song(data["artist"], data["song"], TaskState.DOWNLOADED)
            elif song.state == TaskState.DOWNLOADED:
                song.vocals_path = song.separate(song.download_path)
                self.add_song(data["artist"], data["song"], TaskState.SEPARATED)
            elif song.state == TaskState.SEPARATED:
                song.lyrics = song.transcribe(song.vocals_path)
                self.add_song(data["artist"], data["song"], TaskState.TRANSCRIBED)
            elif song.state == TaskState.TRANSCRIBED:
                self.add_song(data["artist"], data["song"], TaskState.FINISHED)
            elif song.state == TaskState.FINISHED:
                print(f"Processing Finished: {data['artist']} - {data['song']}")
            else:
                print("Unknown Error has occurred.")
        except queue.Empty:
            print("Empty Song Queue")
        except Exception as e:
            print(f"Error: {e}")
            self.song_queue.put(song)