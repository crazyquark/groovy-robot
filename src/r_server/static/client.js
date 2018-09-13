'use strict';

function connect(host) {
    var ws = new WebSocket('ws://' + host + '/ws');
    ws.onopen = () => {
        console.log('connected to server');
        ws.send('1');
    };

    ws.onmessage = (event) => {
        let msg = event.data
        document.getElementById('cam')
            .setAttribute('src', 'data:image/jpg;base64,' + msg);
        ws.send('1');
    };

    ws.onclose = () => {
        console.log('server connection lost')

        document.removeEventListener('keydown', keydownHandler, false);
        document.removeEventListener('keyup', keyupHandler, false);

        connect(host);
    };

    var sendKey = (keyName) => {
        if (keyName === 'w' || keyName === 'ArrowUp') {
            ws.send('w');
        } else if (keyName === 's' || keyName === 'ArrowDown') {
            ws.send('s');
        } else if (keyName === 'a' || keyName === 'ArrowLeft') {
            ws.send('a');
        } else if (keyName === 'd' || keyName === 'ArrowRight') {
            ws.send('d');
        } else {
            ws.send(keyName);
        }
    };

    var keydownHandler = (event) => {
        // Ignore repeated events FFS
        if (event.repeat) {
            return;
        }

        const keyName = event.key.toLowerCase();

        console.log('down: ' + keyName);

        sendKey(keyName);
    };

    var keyupHandler = (event) => {
        const keyName = event.key.toUpperCase();

        console.log('up: ' + keyName);

        sendKey(keyName);

    };

    var stream_mic = function (host) {
        if (host) {
            var mic_ws = new WebSocket('ws://' + host + '/mic');
            mic_ws.binaryType = 'arraybuffer';

            var audioContext = new(window.AudioContext || window.webkitAudioContext)();

            mic_ws.onopen = () => {
                mic_ws.send('1');
            };
            
            var nextTime = audioContext.currentTime + 0.1;
            mic_ws.onmessage = (event) => {
                audioContext.decodeAudioData(event.data, function (buffer) {
                    var source = audioContext.createBufferSource();
                    source.channelCount = 1;
                    source.buffer = buffer;
                    source.connect(audioContext.destination);
                    source.start(nextTime);

                    nextTime += buffer.duration;
                }, function (err) {
                    console.log(err);
                });

                mic_ws.send('1');
            };
        }
    };

    document.addEventListener('keydown', keydownHandler, true);
    document.addEventListener('keyup', keyupHandler, true);

    stream_mic(host);
}