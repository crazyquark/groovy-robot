'use strict';

function webAudioTouchUnlock(context) {
    return new Promise(function (resolve, reject) {
        if (context.state === 'suspended' && 'ontouchstart' in window) {
            const unlock = function () {
                context.resume().then(function () {
                        document.removeEventListener('touchstart', unlock);
                        document.removeEventListener('touchend', unlock);

                        resolve(true);
                    },
                    function (reason) {
                        reject(reason);
                    });
            };

            document.addEventListener('touchstart', unlock, false);
            document.addEventListener('touchend', unlock, false);
        } else {
            resolve(false);
        }
    });
}

function init_ui() {
    let camera = document.getElementById('camera');
    let joystick = nipplejs.create({
        zone: camera
    });

    let sendKey = window.sendKey;
    if (sendKey === undefined) {
        return;
    }

    let pressed_keys = [];
    joystick.on('dir', (event, data) => {
        let dir = data.direction;
        let key = null;
        switch (dir.angle) {
            case 'up':
                key = 'w';
                break;
            case 'down':
                key = 's';
                break;
            case 'left':
                key = 'a';
                break;
            case 'right':
                key = 'd';
                break;
            default:
                key = null;
        }

        if (key !== null) {
            sendKey(key);
            pressed_keys.push(key);
        }
    });

    joystick.on('end', () => {
        for (let key of pressed_keys) {
            sendKey(key.toUpperCase());
        }

        pressed_keys = [];
    });

    let camPlusButton = document.getElementById('cam+');
    let camMinusButton = document.getElementById('cam-');
    camPlusButton.addEventListener('mousedown', () => {
        sendKey('e');
    });
    camPlusButton.addEventListener('touchstart', () => {
        sendKey('e');
    });
    camPlusButton.addEventListener('mouseup', () => {
        sendKey('E');
    });
    camPlusButton.addEventListener('touchended', () => {
        sendKey('E');
    });

    camMinusButton.addEventListener('mousedown', () => {
        sendKey('q');
    });
    camMinusButton.addEventListener('touchstart', () => {
        sendKey('q');
    });
    camMinusButton.addEventListener('mouseup', () => {
        sendKey('Q');
    });
    camMinusButton.addEventListener('touchended', () => {
        sendKey('Q');
    });

    let spdPlusButton = document.getElementById('spd+');
    let spdMinusButton = document.getElementById('spd-');
    spdPlusButton.addEventListener('mousedown', () => {
        sendKey('x');
    });
    spdPlusButton.addEventListener('touchstart', () => {
        sendKey('x');
    });
    camPlusButton.addEventListener('mouseup', () => {
        sendKey('X');
    });
    camPlusButton.addEventListener('touchended', () => {
        sendKey('X');
    });

    spdMinusButton.addEventListener('mousedown', () => {
        sendKey('z');
    });
    spdMinusButton.addEventListener('touchstart', () => {
        sendKey('z');
    });
    spdMinusButton.addEventListener('mouseup', () => {
        sendKey('Z');
    });
    spdMinusButton.addEventListener('touchended', () => {
        sendKey('Z');
    });
}

function connect(host) {
    const ws = new WebSocket('ws://' + host + '/ws');
    ws.onopen = () => {
        console.log('connected to server');
        ws.send('1');
    };

    ws.onmessage = (event) => {
        let msg = event.data;
        document.getElementById('cam')
            .setAttribute('src', 'data:image/jpeg;base64,' + msg);
        ws.send('1');
    };

    ws.onclose = () => {
        console.log('server connection lost');

        document.removeEventListener('keydown', keydownHandler, false);
        document.removeEventListener('keyup', keyupHandler, false);

        connect(host);
    };

    const sendKey = (keyName) => {
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

    window.sendKey = sendKey;

    const keydownHandler = (event) => {
        // Ignore repeated events FFS
        if (event.repeat) {
            return;
        }

        const keyName = event.key.toLowerCase();

        console.log('down: ' + keyName);

        sendKey(keyName);
    };

    const keyupHandler = (event) => {
        const keyName = event.key.toUpperCase();

        console.log('up: ' + keyName);

        sendKey(keyName);

    };

    const stream_mic = function (host) {
        if (host) {
            const audioContext = new(window.AudioContext || window.webkitAudioContext)();
            webAudioTouchUnlock(audioContext).then(function (unlocked) {
                    if (unlocked) {
                        // AudioContext was unlocked from an explicit user action,
                        // sound should start playing now
                    } else {
                        // There was no need for unlocking, devices other than iOS
                    }
                },
                function (reason) {
                    console.error(reason);
                });

            const micWorker = new Worker('/static/ws-worker.js');

            let nextTime = audioContext.currentTime;
            micWorker.onmessage = (event) => {
                const data = event.data;
                const buffer = audioContext.createBuffer(1, data.length, audioContext.sampleRate);
                buffer.copyToChannel(data, 0);

                const source = audioContext.createBufferSource();
                source.buffer = buffer;

                source.connect(audioContext.destination);
                source.start(nextTime);

                nextTime += buffer.duration;
            };

            // Start stream
            micWorker.postMessage({});
        }
    };

    document.addEventListener('keydown', keydownHandler, true);
    document.addEventListener('keyup', keyupHandler, true);

    stream_mic(host);
}