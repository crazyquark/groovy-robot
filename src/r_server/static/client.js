'use strict'

function connect(host) {
    var ws = new WebSocket('ws://' + host + '/ws');
    ws.onopen = function () {
        ws.send('1');
    };
    
    ws.onmessage = function (event) {
        let msg = event.data
        document.getElementById('cam')
            .setAttribute('src', 'data:image/jpg;base64,' + msg);
        ws.send('1');
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
}
