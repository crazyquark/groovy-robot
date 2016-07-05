<!DOCTYPE html>
<html>
<head>
  <script type="text/javascript">
    'use strict'

	var ws = new WebSocket("ws://{{ host }}/ws");
    ws.onopen = function() {
        ws.send("hello");
    };
    ws.onmessage = function (evt) {
        console.log(evt.data);
    };

	document.addEventListener('keydown', (event) => {
	  const keyName = event.key;
	
	  console.log('down: ' + keyName);

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
	  }
	}, false);

	document.addEventListener('keyup', (event) => {
	  const keyName = event.key;

	  console.log('up: ' + keyName);

	}, false);

  </script>
</head>
</html>