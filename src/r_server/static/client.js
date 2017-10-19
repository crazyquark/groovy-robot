'use strict'

var ws = new WebSocket('ws://{{ host }}/ws');
ws.onopen = function () {
    ws.send('hello');
};
ws.onmessage = function (evt) {
    console.log(evt.data);
};

var sendKey = (keyName) => {
    if (keyName === 'w' || keyName === 'ArrowUp') {
        ws.send('w');
    }
    else if (keyName === 's' || keyName === 'ArrowDown') {
        ws.send('s');
    }
    else if (keyName === 'a' || keyName === 'ArrowLeft') {
        ws.send('a');
    }
    else if (keyName === 'd' || keyName === 'ArrowRight') {
        ws.send('d');
    } else {
        ws.send(keyName)
    }
};

var keydownHandler = (event) => {
    // Ignore repeated events FFS
    if (event.repeat) {
        return
    }

    const keyName = event.key.toLowerCase();

    console.log('down: ' + keyName)

    sendKey(keyName)
};

var keyupHandler = (event) => {
    const keyName = event.key.toUpperCase();

    console.log('up: ' + keyName)

    sendKey(keyName)

};

document.addEventListener('keydown', keydownHandler, false);
document.addEventListener('keyup', keyupHandler, false);