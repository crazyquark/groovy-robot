
onmessage = function () {
    const websocket = new WebSocket(`ws://${self.location.host}/mic`);
    websocket.binaryType = 'arraybuffer';

    websocket.onopen = () => {
        websocket.send('1');
    };

    websocket.onmessage = (event) => {
        const data = new Float32Array(event.data);
        
        postMessage(data);

        websocket.send('1');
    };
};
