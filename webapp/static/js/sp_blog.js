function getPost(id) {
    var xmlhttp = new XMLHttpRequest();
    var url = 'http://larby.co.uk/sp-post?src=js&post=' + id;

    xmlhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var myArr = JSON.parse(this.responseText);
            display(myArr);
        }
    };

    xmlhttp.open("GET", url, true);
    xmlhttp.send();
}

function display(arr) {
    var out = arr["html_content"];
    document.getElementById("sp_blog_content").innerHTML = out;
}

function get_sp_post(id) {
    var url = 'http://larby.co.uk/sp-post?src=js&post=' + id;
    fetch(url)
        .then(response => response.json())
        .then(data => {
            var myArr = JSON.parse(data);
            display(myArr);
        });
}