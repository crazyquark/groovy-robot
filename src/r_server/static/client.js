'use strict';

class RobotClient {
    constructor() {
    }

    initUI() {
        let camera = document.getElementById('camera');
        let joystick = nipplejs.create({
            zone: camera
        });

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
                this._sendKey(key);
                pressed_keys.push(key);
            }
        });

        joystick.on('end', () => {
            for (let key of pressed_keys) {
                this._sendKey(key.toUpperCase());
            }

            pressed_keys = [];
        });

        let camPlusButton = document.getElementById('cam+');
        let camMinusButton = document.getElementById('cam-');
        camPlusButton.addEventListener('mousedown', () => {
            this._sendKey('e');
        });
        camPlusButton.addEventListener('touchstart', () => {
            this._sendKey('e');
        });
        camPlusButton.addEventListener('mouseup', () => {
            this._sendKey('E');
        });
        camPlusButton.addEventListener('touchended', () => {
            this._sendKey('E');
        });

        camMinusButton.addEventListener('mousedown', () => {
            this._sendKey('q');
        });
        camMinusButton.addEventListener('touchstart', () => {
            this._sendKey('q');
        });
        camMinusButton.addEventListener('mouseup', () => {
            this._sendKey('Q');
        });
        camMinusButton.addEventListener('touchended', () => {
            this._sendKey('Q');
        });

        let spdPlusButton = document.getElementById('spd+');
        let spdMinusButton = document.getElementById('spd-');
        spdPlusButton.addEventListener('mousedown', () => {
            this._sendKey('x');
        });
        spdPlusButton.addEventListener('touchstart', () => {
            this._sendKey('x');
        });
        camPlusButton.addEventListener('mouseup', () => {
            this._sendKey('X');
        });
        camPlusButton.addEventListener('touchended', () => {
            this._sendKey('X');
        });

        spdMinusButton.addEventListener('mousedown', () => {
            this._sendKey('z');
        });
        spdMinusButton.addEventListener('touchstart', () => {
            this._sendKey('z');
        });
        spdMinusButton.addEventListener('mouseup', () => {
            this._sendKey('Z');
        });
        spdMinusButton.addEventListener('touchended', () => {
            this._sendKey('Z');
        });
    }

    connect() {
        const socket = io('/control');
        socket.on('connect', () => {
            console.log('Connected to control socket');
        });
        socket.on('disconnect', () => {
            console.log('Disconnected from control socket');

            this.connect();
            // worker.terminate();
        });

        socket.on('status', (event) => {
            if (event === 'connected') {
                console.log('Server confirmed connection');
                this._setupKeyHandlers(socket);
            }
        });


        // const worker = stream_mic();
    }

    _sendKey = (socket, keyName) => {
        if (keyName === 'w' || keyName === 'ArrowUp') {
            socket.emit('control_key', 'w');
        } else if (keyName === 's' || keyName === 'ArrowDown') {
            socket.emit('control_key', 's');
        } else if (keyName === 'a' || keyName === 'ArrowLeft') {
            socket.emit('control_key', 'a');
        } else if (keyName === 'd' || keyName === 'ArrowRight') {
            socket.emit('control_key', 'd');
        } else {
            socket.emit('control_key', keyName);
        }
    };

    _setupKeyHandlers(socket) {
        const keydownHandler = (event) => {
            // Ignore repeated events FFS
            if (event.repeat) {
                return;
            }
            const keyName = event.key.toLowerCase();
            console.log('down: ' + keyName);
            this._sendKey(socket, keyName);
        };
        const keyupHandler = (event) => {
            const keyName = event.key.toUpperCase();
            console.log('up: ' + keyName);
            this._sendKey(socket, keyName);
        };
        document.addEventListener('keydown', keydownHandler, true);
        document.addEventListener('keyup', keyupHandler, true);
    }

    _streamMic() {
        const audioContext = new (window.AudioContext || window.webkitAudioContext)();
        this._webAudioTouchUnlock(audioContext).then(function (unlocked) {
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

        return micWorker;
    }

    _webAudioTouchUnlock(context) {
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
}
