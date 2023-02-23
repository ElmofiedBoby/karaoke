import time
from taskstate import TaskState
from Pipeline import Pipeline


pipeline = Pipeline()
print("Pipeline loaded!")

pipeline.add_song('Taylor Swift', 'Enchanted', TaskState.QUEUED)
while(True):
    time.sleep(3)
    pipeline.add_task()