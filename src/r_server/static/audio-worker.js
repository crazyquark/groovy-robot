
onmessage = function (io) {
    const audioWebsocket = io('/audio');
    audioWebsocket.on('connect', () => {
        console.log('Connected to audio socket');
    });

    audioWebsocket.on('data', (event) => {
        console.log(event);
    });
};
