let playlist;
let quizlist = [];
let search_result = [];
const msg = new SpeechSynthesisUtterance(); //come from WEB Speech API
let voices = [];
const voicesDropdown = document.querySelector('[name="voice"]');
const options = document.querySelectorAll('[type="range"], [name="text"]');
const speakButton = document.querySelector('#speak');
const stopButton = document.querySelector('#stop');
const answerButton = document.querySelector('#answer');
const search_playlistButton = document.querySelector('#search_playlist');
msg.text = document.querySelector('[name="text"]').value;

function populateVoices() {
    voices = this.getVoices();
    console.log(voices);
    voicesDropdown.innerHTML = voices
        .map(voice => `<option value="${voice.name}">${voice.name} (${voice.lang})</option>`)
        .join('');
    document.getElementById("voices").selectedIndex = 25;
}

speechSynthesis.addEventListener('voiceschanged', populateVoices);

function toggle(startOver = true) {
    speechSynthesis.cancel(); // stop speaking
    if (startOver) {
        speechSynthesis.speak(msg); // restart speaking
    }
}

function setVoice() {
    console.log('changing voice');
    msg.voice = voices.find(voice => voice.name === this.value);
    toggle();
}

voicesDropdown.addEventListener('change', setVoice);

function setOption() {
    console.log(this.name, this.value);
    msg[this.name] = this.value;
    toggle();
}

function get_quiz_list(playlist_id) {
    document.getElementById('speak').style.visibility = 'hidden';
    document.getElementById('stop').style.visibility = 'hidden';
    playlist = ajax_url("get_quiz/" + playlist_id)['tracks']['data']
    document.getElementById('speak').style.visibility = 'visible';
    document.getElementById('stop').style.visibility = 'visible';
}
function speak() {
    hide_answer()
    if (playlist.length == quizlist.length) {
        alert("出題完畢")
    } else {
        random = Math.floor(Math.random() * playlist.length)
        while (quizlist.includes(random)) {
            random = Math.floor(Math.random() * playlist.length)
        }
        quiz = playlist[random]
        quizlist.push(random)
        set_answer();
        console.log(quiz['album']['artist']['name'], quiz['name'])
        singer = quiz['album']['artist']['name'].split(' ')[0]
        song = quiz['name'].split(' ')[0]
        data = ajax_url("get_lyric/" + singer + "/" + song)
        console.log(data)
        if (data == 'Something error') {
            speak()
        } else {
            document.getElementById("lyrics").innerHTML = data
            msg.text = document.querySelector('[name="text"]').value;
            toggle()
        }
    }
}
function set_answer() {
    document.getElementById("song_name_text").innerHTML = quiz['name'];
    document.getElementById("singer_text").innerHTML = quiz['album']['artist']['name'];
    document.getElementById("album_name_text").innerHTML = quiz['album']['name'];
    document.getElementById("album").src = quiz['album']['images'][0]['url'];
    document.getElementById("release_date_text").innerHTML = quiz['album']['release_date'];
}
function show_answer() {
    document.getElementById("song_name_text").style.visibility = "visible";
    document.getElementById("singer_text").style.visibility = "visible";
    document.getElementById("album_name_text").style.visibility = "visible";
    document.getElementById("album").style.visibility = "visible";
    document.getElementById("release_date_text").style.visibility = "visible";
}
function hide_answer() {
    document.getElementById("song_name_text").style.visibility = "hidden";
    document.getElementById("singer_text").style.visibility = "hidden";
    document.getElementById("album_name_text").style.visibility = "hidden";
    document.getElementById("album").style.visibility = "hidden";
    document.getElementById("release_date_text").style.visibility = "hidden";
}

function search_playlist() {
    playlist_result = document.getElementById("playlist_result");
    playlist_result.innerText = null;	//清空下拉選單
    keyword = document.querySelector("#playlist_search").value;
    search_result = ajax_url("search_playlist/" + keyword)['data']['result']
    for (var i = 0; i < search_result.length; i++) {    //把結果塞入playlist_result的下拉選單中
        var opt = search_result[i]['title'];
        var el = document.createElement("option");
        el.textContent = opt;
        el.value = opt;
        playlist_result.appendChild(el);
    }
    get_quiz_list(search_result[0]['id'])
    document.getElementById('playlist_comefrom').style.visibility = 'visible';
    document.getElementById('playlist_comefrom').href = search_result[0]['url']
}
function ajax_url(url) {	//get data using jquery.ajax
    var result;
    $.ajax({
        url: url,
        datatype: 'json',
        async: false,
        success: function (data) {
            result = data;
        }
    });
    return result
}

options.forEach(option => option.addEventListener('change', setOption))

speakButton.addEventListener('click', speak);
stopButton.addEventListener('click', () => toggle(false));
answerButton.addEventListener('click', show_answer);
search_playlistButton.addEventListener('click', search_playlist);
playlist_result = document.getElementById("playlist_result");
playlist_result.addEventListener("change", function () {	//playlist_result的下拉選單有變化時
    document.getElementById('set_quiz').style.visibility = 'hidden';
    seleted = playlist_result.selectedIndex
    get_quiz_list(search_result[seleted]['id'])
    document.getElementById('playlist_comefrom').style.visibility = 'visible';
    document.getElementById('playlist_comefrom').href = search_result[seleted]['url']
});