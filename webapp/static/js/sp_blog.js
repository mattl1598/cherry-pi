function get_sp_post(id) {
    var url = 'http://larby.co.uk/sp-post?post=' + id + '&src=js';
    fetch(url)
        .then(response => response.json())
        .then(data => {
            return data;
        });
}