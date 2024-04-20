# Open Source Karaoke Software

Web:
- Request: Download song/title [Broker]
- Request: Song list [Broker]
- Request: Song metadata [Broker]

Broker:
- Request: Song lyrics [azlyricsapi]
- Request: Song metadata [yt-dlp]
- Request: Song enhancement [Enhancer]
- Request: Song alignment [Aligner]
- Response: song download status [Interface]
- Response: Song list [Interface]
- Response: Song metadata [Interface]

Enhancer:
- Response: Enhanced audio filepaths [Broker]

Aligner:
- Response: Aligned filepaths [Broker]

Metadata:
- Song name
- Song artist
- Song album
- Song duration in seconds
- Song format
- Song original audio filepath
- Song vocals audio filepath
- Song background audio filepath
- Song lyrics
- Song timed lyrics