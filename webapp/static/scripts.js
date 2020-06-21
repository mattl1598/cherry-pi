function key_64(length) {
	var url = 'http://127.0.0.1:5000/bse64/' + length;
	console.log(url);
    fetch(url)
        .then(response => response.json())
		.then(data => {
			console.log(data);
			console.log(data.key);
			return data.key;
         });
}

function clip_text(a_string){
    var input = document.createElement('input');
    input.id="__copyText__";
    input.value = a_string;
    document.body.appendChild(input);
    input.select();
    document.execCommand("copy");
    var txt = input.value;
    input.remove();
    console.log("OK COPIED: '"+txt+"'");
}

function clip_key_64() {
	data = key_64(64);
	console.log(data);
	clip_text(data);
}