$(document).ready(function() {
     $('#step1form').fadeIn(500);
})

function serialize (data) {
	let obj = {};
	for (let [key, value] of data) {
		if (obj[key] !== undefined) {
			if (!Array.isArray(obj[key])) {
				obj[key] = [obj[key]];
			}
			obj[key].push(value);
		} else {
			obj[key] = value;
		}
	}
	return obj;
}

function post(nextstep, serialized, loading) {
    $.ajax({
         type: 'POST',
         url: '/',
         data: JSON.stringify(serialized),
         contentType: 'application/json',
         dataType: 'json',
         success: function(response) {
            loading.html('');
            $(nextstep+'form').html(response);
            $(nextstep+'form').fadeIn(500)
            },
         error: function(response) {console.log("ERROR", response)}
         })
}

function send(step) {
   event.preventDefault();
   let nextstep = '#step' + (step + 1)
   let loading = $(nextstep+'loading');
   let form = $('#step'+step+'form').get(0);
   let data = new FormData(form);
   let serialized = serialize(data);
   $(nextstep+'form').get(0).innerHTML = '';
   $(nextstep+'form').fadeOut(0);
   loading.html('Loading...');
   if (data.has('file')) {
       const file = data.get('file');
	   const datafile = new FormData();
       datafile.append('file', file);
       fetch('/uploads', {
                method: 'POST',
                body: datafile
            })
            .then(response => response.json())
            .then(data => {
                console.log(data);
                serialized['filename']=data['filename'];
                post(nextstep, serialized, loading)
                })
            .catch(error => {alert(error)});
       }
   else {
       post(nextstep, serialized, loading);
   }
   $(nextstep).get(0).scrollIntoView({behavior: 'smooth'});
}

function toggleText(start, end, text){
    let element = document.getElementById("text");
    let str = start+'-'+end+'('+text+');';
    if (element.value.includes(str)) {
        element.value = element.value.replace(str, '')
    } else {
        element.value += str;
    }
}

function filterLevel(){
    let value = document.getElementById("range").value;
    for (el of document.getElementById("words").children) {
        if (el.value > 1-value) {el.style.color="red"} else {el.style.color="#212529"}
    }
}

function clearText(){
    document.getElementById("text").value = "";
    for (el of document.getElementById("words").children) {
        el.classList.remove("active");
    }
}

function addWords(){
    clearText();
    let value = document.getElementById("range").value;
    for (el of document.getElementById("words").children) {
        if (el.value > 1-value) {el.click()}
    }
}