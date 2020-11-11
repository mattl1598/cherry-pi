function getPost(id=0, preview="false") {
    if (id >= 0) {
        var xmlhttp = new XMLHttpRequest();
        var url = 'http://larby.co.uk/sp-post?src=js&post=' + id + "&preview=" + preview;

        xmlhttp.onreadystatechange = function () {
            if (this.readyState == 4 && this.status == 200) {
                var myArr = JSON.parse(this.responseText);
                display(myArr);
            }
        };

        xmlhttp.open("GET", url, true);
        xmlhttp.send();
    } else {
        display({"html_content": "Error"})
    }
}

function display(arr) {
    var out = arr["html_content"];
    var title = "Thespian Life in Lockdown - " + arr["title"];
    document.getElementsByClassName("entry-title").innerHTML = title;
    document.getElementById("sp_blog_content").innerHTML = out;
}
