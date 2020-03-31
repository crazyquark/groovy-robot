
onmessage = function () {
    fetch('/audio').then(response => response.body)
    .then(rs => {
        const reader = rs.getReader();
        const processData = (done, data) => {
            postMessage(new Float32Array(data));

            if (done) {
                return;
            }
    
            return reader.read().then(processData);
        };

        reader.read.then(processData);
    });
};
