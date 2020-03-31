
onmessage = function () {
    fetch('/audio')
    .then(response => {
        const reader = response.body.getReader();
        const processData = ({done, value}) => {
            const data = new Float32Array(value)
            if (data.length > 0) {
                postMessage(data);
            }

            if (done) {
                return;
            }
    
            return reader.read().then(processData);
        };

        reader.read().then(processData);
    });
};
