var audio1 = document.getElementById('audio1');
var audio2 = document.getElementById('audio2');
var seekbar = document.getElementById('seekbar');
var volume1 = document.getElementById('volume1');
var volume2 = document.getElementById('volume2');
var play = document.getElementById('play');
var pause = document.getElementById('pause');
var lyricsContainer = document.getElementById('lyrics-container');
var timestamp = document.getElementById('time-stamp');
var playing = false;
var lrcData = null;
var seekbarDragging = false;
var artist = document.getElementById('artist');
var song = document.getElementById('song');
var queue = []
var html = '';

function loadLRCFile() {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', "/lyrics?artist="+artist.innerText+"&song="+song.innerText, true);
    xhr.onreadystatechange = function() {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 200) {
                lrcData = xhr.responseText
                console.log('LRC file loaded successfully');
                populateQueue();
            } else {
                console.log('Failed to load LRC file');
            }
        }
    };
    xhr.send();
}

function populateQueue() {
    console.log("Populating Queue...");
    if (!lrcData) {
        return;
    }

    var lines = lrcData.split('\n');

    for (var i = 0; i < lines.length; i++) {
        var line = lines[i].trim();
        var match = line.match(/\[(\d+:\d+)\]\[(\d+:\d+)\](.*)/);

        if (match) {
            var startTime = match[1];
            var endTime = match[2];
            var lyrics = match[3];

            var startTimeInSeconds = convertTimeToSeconds(startTime);
            var endTimeInSeconds = convertTimeToSeconds(endTime);

            queue.push({
                time: startTimeInSeconds,
                endTime: endTimeInSeconds,
                lyrics: lyrics
            });
        }
    }
    console.log("Queue population complete!");
}

function displayLyrics() {
    var currentTime = parseInt(audio1.currentTime);
    var start = 0;
    var end = queue.length - 1;

    while (start <= end) {
        var mid = Math.floor((start + end) / 2);
        var item = queue[mid];

        if (item.time <= currentTime) {
            //console.log(item.time +"|"+item.endTime+"|"+currentTime)
            html = item.lyrics + '<br>';
            start = mid + 1;
        } else {
            end = mid - 1;
        }
    }

    lyricsContainer.innerHTML = html;
}

function convertTimeToSeconds(time) {
    var parts = time.split(':');
    var minutes = parseInt(parts[0]);
    var seconds = parseFloat(parts[1]);
    return minutes;
}

function convertSecondsToTime(val) {
    var minute;
    var second;

    if(val < 60) {
        minute = 0;
        if(val<10) {
            second = "0"+parseInt(val);
        }
        else {
            second = parseInt(val);
        }
    }
    else {
        minute = parseInt(val / 60);
        val = val - (minute*60)
        if(val<10) {
            second = "0"+parseInt(val);
        }
        else {
            second = parseInt(val);
        }
    }
    return minute+":"+second;
}

loadLRCFile();

console.log(audio1);

audio1.addEventListener('loadedmetadata', function() {
    seekbar.max = audio1.duration;
});

audio2.addEventListener('loadedmetadata', function() {
    seekbar.max = audio2.duration;
});

audio1.addEventListener('timeupdate', function() {
    audio1Duration = audio1.duration;
    audio1CurrentTime = audio1.currentTime;
    seekbar.value = audio1CurrentTime;
    timestamp.innerHTML = convertSecondsToTime(seekbar.value)+"/"+convertSecondsToTime(seekbar.max);
    displayLyrics();
});

seekbar.addEventListener('input', function() {
    audio1.currentTime = seekbar.value;
    audio2.currentTime = seekbar.value;
});

volume1.addEventListener('input', function() {
    audio1.volume = volume1.value;
});

volume2.addEventListener('input', function() {
    audio2.volume = volume2.value;
});

play.addEventListener('click', function() {
    if (!playing) {
        audio1.play();
        audio2.play();
        playing = true;
    }
});

pause.addEventListener('click', function() {
    if (playing) {
        audio1.pause();
        audio2.pause();
        playing = false;
    }
});
