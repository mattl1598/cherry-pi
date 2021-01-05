const aud = document.getElementById("dw_player");
const viewSent = document.getElementById("viewSent");
const seeked = document.getElementById("seeked");

aud.addEventListener("timeupdate", viewCounter);
aud.addEventListener("play", url_query);

aud.onseeked = function() {
    seeked.value = "1";
    aud.removeEventListener("timeupdate", viewCounter);
    set_url_query();
}

function sendView() {
    var xmlhttp = new XMLHttpRequest();
    var url = "http://larby.co.uk/soundcounter/dickwhittington";
    xmlhttp.open("GET", url, true);
    xmlhttp.send();
}

function viewCounter() {
    if ((document.getElementById("viewSent").value !== "1") && (seeked.value !== "1")) {
        let currentTime = aud.currentTime;
        if (currentTime >= 30) {
            viewSent.value = "1";
            aud.removeEventListener("timeupdate", viewCounter);
            sendView();
            set_url_query();
        }
    }
}

function set_url_query() {
    let dateNow = new Date();
    let date2021 = new Date(2021, 1, 1, 0, 0, 0, 0);
    let hours_now = parseInt(diff_hours(dateNow, date2021));
    let d1 = (hours_now * 2) + parseInt(viewSent.value, 10);
    let d = (d1 * 2) + parseInt(seeked.value, 10);
    console.log(hours_now)
    console.log(d1)
    console.log(d)
    let new_url = window.location.href.split("?")[0].concat("?d=").concat(d.toString(10));
    history.replaceState(null, document.title, new_url);
}

function url_query() {
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    let d = urlParams.get('d')
    if (d != null){
        let data = parseInt(d, 10).toString(2);
        let dSeeked = data.charAt(data.length-1);
        let viewed = data.charAt(data.length-2);
        console.log(data);
        console.log(dSeeked);
        console.log(viewed);
        let hours = parseInt(data.substr(0, data.length-2), 2);
        let dateNow = new Date();
        let date2021 = new Date(2021, 1, 1, 0, 0, 0, 0);
        let hours_now = diff_hours(dateNow, date2021);
        let hours_diff = hours_now - hours;
        if (hours_diff >= 3) {
            let new_url = window.location.href.split("?")[0];
            history.replaceState(null, document.title, new_url);
        } else if ((hours_diff < 3) && ((dSeeked === "1") || (viewed === "1"))) {
            aud.removeEventListener("timeupdate", viewCounter);
            aud.removeEventListener("play", url_query);
            seeked.value = dSeeked;
            viewSent.value = viewed;
        }
    }
}

function diff_hours(dt2, dt1) {
  var diff =(dt2.getTime() - dt1.getTime()) / 1000;
  diff /= 60;
  diff /= 60;
  return Math.abs(Math.round(diff));
}