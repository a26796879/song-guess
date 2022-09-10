let playlist;
let quizlist = [];
const msg = new SpeechSynthesisUtterance(); //come from WEB Speech API
let voices = [];
// const voicesDropdown = document.querySelector('[name="voice"]');
// const options = document.querySelectorAll('[type="range"], [name="text"]');
// const speakButton = document.querySelector('#speak');
// const stopButton = document.querySelector('#stop');
const get_playlistButton = document.querySelector('#get_playlist');
const setQuizButton = document.querySelector('#set_quiz');
const answerButton = document.querySelector('#answer');
// msg.text = document.querySelector('[name="text"]').value;

// function populateVoices() {
//     voices = this.getVoices();
//     console.log(voices);
//     voicesDropdown.innerHTML = voices
//         .map(voice => `<option value="${voice.name}">${voice.name} (${voice.lang})</option>`)
//         .join('');
// }

// speechSynthesis.addEventListener('voiceschanged', populateVoices);

// function toggle(startOver = true) {
//     speechSynthesis.cancel(); // stop speaking
//     if (startOver) {
//         speechSynthesis.speak(msg); // restart speaking
//     }
// }

// function setVoice() {
//     console.log('changing voice');
//     msg.voice = voices.find(voice => voice.name === this.value);
//     toggle();
// }

// voicesDropdown.addEventListener('change', setVoice);

// function setOption() {
//     console.log(this.name, this.value);
//     msg[this.name] = this.value;
//     toggle();
// }

function get_quiz_list() {
    playlist_id = document.querySelector("#playlist_id").value;
    playlist = ajax_url("get_quiz/" + playlist_id)['tracks']['data']
    console.log(playlist)
}
function set_quiz() {
    hide_answer()
    var video = document.getElementById('video');
    video.pause();
    if (playlist.length == quizlist.length) {
        alert("出題完畢")
    } else {
        random = Math.floor(Math.random() * playlist.length)
        while (quizlist.includes(random)) {
            random = Math.floor(Math.random() * playlist.length)
        }
        quiz = playlist[random]
        quizlist.push(random)
        data = ajax_url("get_preview/" + quiz['id'])
        document.getElementById("video").src = data['preview_url'];
        video.load();
        video.play();
        set_answer();
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

// options.forEach(option => option.addEventListener('change', setOption))

// speakButton.addEventListener('click', toggle);
// stopButton.addEventListener('click', () => toggle(false));
setQuizButton.addEventListener('click', set_quiz);
answerButton.addEventListener('click', show_answer);
get_playlistButton.addEventListener('click', get_quiz_list);
