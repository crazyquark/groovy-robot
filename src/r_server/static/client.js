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

        this._setupKeyHandlers();

        // Start image processing
        this._setupAI();
    }

    connect() {
        this.socket = io('/control');
        this.socket.on('connect', () => {
            console.log('Connected to control socket');
        });
        this.socket.on('disconnect', () => {
            console.log('Disconnected from control socket');

            this.connect();
            // worker.terminate();

        });

        this.socket.on('status', (event) => {
            if (event === 'connected') {
                console.log('Server confirmed connection');
            }
        });

        this._streamMic();
    }

    _sendKey = (keyName) => {
        if (keyName === 'w' || keyName === 'ArrowUp') {
            this.socket.emit('control_key', 'w');
        } else if (keyName === 's' || keyName === 'ArrowDown') {
            this.socket.emit('control_key', 's');
        } else if (keyName === 'a' || keyName === 'ArrowLeft') {
            this.socket.emit('control_key', 'a');
        } else if (keyName === 'd' || keyName === 'ArrowRight') {
            this.socket.emit('control_key', 'd');
        } else {
            this.socket.emit('control_key', keyName);
        }
    };

    _setupKeyHandlers() {
        const keydownHandler = (event) => {
            // Ignore repeated events FFS
            if (event.repeat) {
                return;
            }
            const keyName = event.key.toLowerCase();
            console.log('down: ' + keyName);
            this._sendKey(keyName);
        };
        const keyupHandler = (event) => {
            const keyName = event.key.toUpperCase();
            console.log('up: ' + keyName);
            this._sendKey(keyName);
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

        // const micWorker = new Worker('/static/audio-worker.js');
        const audioWebsocket = io('/audio');
        audioWebsocket.on('connect', () => {
            console.log('Connected to audio socket');
        });

        let nextTime = audioContext.currentTime;
        audioWebsocket.on('data', (data) => {
            nextTime = this._playAudio(data, audioContext, nextTime);
        });

        // micWorker.onmessage = (event) => {
        // };

        // Start stream
        // micWorker.postMessage(io);

        // return micWorker;
    }

    _playAudio(data, audioContext, nextTime) {
        data = new Float32Array(data)
        const buffer = audioContext.createBuffer(1, data.length, audioContext.sampleRate);
        buffer.copyToChannel(data, 0);

        const source = audioContext.createBufferSource();
        source.buffer = buffer;
        source.connect(audioContext.destination);
        source.start(nextTime);
        nextTime += buffer.duration;

        return nextTime;
    }

    _setupAI() {
        const canvas = document.getElementById('overlay');
        if (!canvas) {
            // If the canvas was not yet loaded, try again later
            setTimeout(() => {
                this._setupAI();
            }, 500);

            return;
        }

        const ctx = canvas.getContext('2d');
        canvas.width = 640;
        canvas.height = 480;

        // Load model
        cocoSsd.load('lite_mobilenet_v2').then(model => {
            const font = "16px sans-serif";
            ctx.font = font;
            ctx.textBaseline = 'top';

            // Detect objects in the image.
            const redraw = () => {
                ctx.clearRect(0, 0, canvas.width, canvas.height);

                model.detect(video).then(predictions => {
                    for (const prediction of predictions) {
                        // {bbox, class, score}
                        const x = prediction.bbox[0];
                        const y = prediction.bbox[1];
                        const width = prediction.bbox[2];
                        const height = prediction.bbox[3];

                        ctx.strokeStyle = 'blue';
                        ctx.strokeRect(x, y, width, height);

                        prediction.class = prediction.class.toUpperCase();

                        ctx.fillStyle = 'green';
                        const textWidth = ctx.measureText(prediction.class).width;
                        const textHeight = parseInt(font, 10); // base 10
                        ctx.fillRect(x, y, textWidth + 4, textHeight + 4);

                        ctx.fillStyle = 'red';
                        ctx.fillText(prediction.class, x + 2, y + 2);
                    }

                    requestAnimationFrame(redraw);
                });
            };
            
            requestAnimationFrame(redraw);
        });
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
