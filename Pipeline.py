from song import Song
from task import TaskState, Task
from dotenv import dotenv_values

import queue
import whisper
import json
import os

from MediaService import MediaService

class Pipeline:

    def __init__(self):
        # Create an event queue
        self.task_queue = queue.Queue()
        self.model = whisper.load_model("small")
        config = dotenv_values(".env")
        self.ms = MediaService(config["youtube_key"], config["path"], config["format"], config["codec"], config["quality"])
        self.song_list = self.populate_list()
        print("Initialized!")

    def populate_list(self):
        song_list = []
        demucs_folder = os.listdir("separated/htdemucs_ft")
        demucs_folder.remove(".music")

        lyric_folder = [song_name.replace('.lrc', '') for song_name in os.listdir("lrc")]
        finished_songs = list(set(demucs_folder) & set(lyric_folder))

        for item in finished_songs:
            parts = item.split("-")
            song_list.append(Song(parts[0].strip(), parts[1].strip(), self.ms, self.model, TaskState.FINISHED))

        return song_list
        
    def add_song(self, artist, song, state):
        song = Song(artist, song, self.ms, self.model, state)
        self.song_list.append(song)
        self.add_task(self.song_list[len(self.song_list)-1])
        print(f'{artist} - {song.song}: {state}')  

    def add_task(self, song):
        task = Task(song)
        self.task_queue.put(task)

    def get_queue(self):
        return self.task_queue

    def run(self):

        try:
            task = self.task_queue.get()
            print(self.song_list)

            if task.state == TaskState.QUEUED:
                task.song.download_path = task.song.download()
                for item in self.song_list:
                    if item.artist == task.song.artist and item.song == task.song.song:
                        item.state = task.song.state
                self.add_task(task.song)
            elif task.state == TaskState.DOWNLOADED:
                task.song.vocals_path = task.song.separate(task.song.download_path)
                for item in self.song_list:
                    if item.artist == task.song.artist and item.song == task.song.song:
                        item.state = task.song.state
                self.add_task(task.song)
            elif task.song.state == TaskState.SEPARATED:
                task.song.lyrics = task.song.transcribe(task.song.vocals_path)
                for item in self.song_list:
                    if item.artist == task.song.artist and item.song == task.song.song:
                        item.state = task.song.state
                self.add_task(task.song)
            elif task.song.state == TaskState.TRANSCRIBED:
                task.song.state = TaskState.FINISHED
                for item in self.song_list:
                    if item.artist == task.song.artist and item.song == task.song.song:
                        item.state = task.song.state
                self.add_task(task.song)
            elif task.song.state == TaskState.FINISHED:
                print(f"Processing Finished: {task.song.artist} - {task.song.song}")
            else:
                task.song.state = TaskState.FINISHED
                print("Unknown Error has occurred.")
                self.add_task(task.song)
        except queue.Empty:
            print("Empty Song Queue")
        except Exception as e:
            print(f"Error: {e}")
            self.add_task(task.song)