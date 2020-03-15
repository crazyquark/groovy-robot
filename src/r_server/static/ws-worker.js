
onmessage = function () {
    const websocket = new WebSocket(`ws://${self.location.hostname}:${self.location.port}/mic`);
    websocket.binaryType = 'arraybuffer';

    websocket.onopen = () => {
        websocket.send('1');
    };

    websocket.onmessage = (event) => {
        const data = event.data;
        postMessage(data);
    };
};