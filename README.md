# Web-based Karaoke Software
Have you ever wanted to sing karaoke, only to find that the only thing you can focus on is the weird discrepancies in the cover of your favorite song? Or maybe your favorite song couldn't be found all together?
This turn-key karaoke solution will ease your worries! Included is a web interface frontend, as well as a backend handling all of the heavy lifting.

## Features

 1. Library
	 - You can add by song, album, or artist
 2. Vocals & Instrumental Isolation
	- Ability to toggle vocals and instrumentals separately
	- Generated via demucs (facebook research labs)
 3. Lyrics (of course)
	- Displays up to five lines at a time, and highlights the line you are on.
	- In the future, highlighting the specific word or utterance you are on will be supported
	- Lyrics are from Genius' API
	- Alignment via NeMo (nvidia)

## Program Workflow
- WEB UI: User searches for a song, and it is added to the queue.
	- If an artist or album, everything under it will be recursively selected and added to the queue.
	- Queue will be transformed into JSON and sent to download service.
	- Frontend will interact with Genius API
- COMM: Database update, notifying downloader
	1. POST song information to DB.
		- Name, Artist, Album, Year, Lyrics
		- Album Covers, Artist Pictures
		- Other misc. metadata
		- Status
			- Unprocessed/Error
			- Downloading/Downloaded
			- Isolating/Isolated
			- Aligning/Aligned
			- Processed/Imported
	2. Publish download request
		- send song metadata (db_id, lyrics)
- Downloader: Download song, send filepath
	- Update status to downloading
	- Utilize YT-DLP to download query and download song
	- Update status to downloaded and filepath
	- Publish isolate request (db id, lyrics, filepath)
- Isolater: Separate song, save, send filepath
	- Update status to isolating
	- Run model
	- Update status to isolated
	- Publish align request (db id, lyrics, filepath, vocals, instrumentals)
- Aligner: Align song, save, send filepath
	- Update status to aligning
	- Run model
	- Update status to aligned
	- Publish import request (db id, lyrics, filepath, vocals, instrumentals, timed_lyrics)
- COMM: Update database, update UI
	- Update status to Processed
	- Update DB with data
	- Update status to Imported
- WEBUI: Library shows all songs with status 'Imported'
	- Use websocket on the 'library' section of web UI so that it is constantly up to date with all songs.
	- When song is chosen, vocals, instrumentals, and timed lyrics are retrieved from db