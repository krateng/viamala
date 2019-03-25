
var localisation = {};

function pageLoad() {
	listVideos();
}

/* file select stuff */

	/* file select with button*/
	 function copyText() {
		 filename = document.getElementById("fileupload").value;
		 filename = filename.split(/[\\/]/).slice(-1)[0];
		 document.getElementById("fake_fileupload").value = filename;
	 }


	 /* drag file onto field */
	 function dragover(evt) {
				 evt.preventDefault();
	 }
	 function readFile(evt) {
		 evt.preventDefault();
		 //var fl = document.getElementById("fileupload").value;
		 var files = evt.dataTransfer.files;
		 //document.getElementById("dropzone").innerHTML = file.name;
		 document.getElementById("fileupload").files = files;


	 }


	 /* actual upload (only on button click) */
	 function uploadFile() {

		 try {
			 videofile = document.getElementById("fileupload").files[0];
			ext = videofile.name.split(".").slice(-1)[0];
			name = videofile.name;

			document.getElementById("status").innerHTML = localisation["ADDVIDEO"];

		 }
		 catch {
			 document.getElementById("status").innerHTML = localisation["ERROR_NOFILE"];
			 window.setTimeout(clear,2000);
			 return;
		 }

		 cut_from = document.getElementById("from").checked;
		 cut_to = document.getElementById("to").checked;

			from_hours = document.getElementById("from_hours").value;
			from_minutes = document.getElementById("from_minutes").value;
			from_seconds = document.getElementById("from_seconds").value;
			to_hours = document.getElementById("to_hours").value;
			to_minutes = document.getElementById("to_minutes").value;
			to_seconds = document.getElementById("to_seconds").value;

			fromtime = from_hours + "-" + from_minutes + "-" + from_seconds;
			totime = to_hours + "-" + to_minutes + "-" + to_seconds;

		 timekeys = ""
		 if (cut_from) {
			 timekeys += "&cutfrom=" + fromtime;
		 }

		 if (cut_to) {
			 timekeys += "&cutto=" + totime;
		 }

		 if (!cut_from && !cut_to) {
			 document.getElementById("status").innerHTML = localisation["ERROR_NOCHANGE"];
			 window.setTimeout(clear,2000);
			 return
		 }


		 try {
			 req = new XMLHttpRequest();
			 req.onreadystatechange = uploadDone;
			 req.open("POST","/upload?name=" + name + timekeys, true);
			 req.send(videofile);
		 }
		 catch {
			 document.getElementById("status").innerHTML = localisation["ERROR_GENERIC"];
			 window.setTimeout(clear,2000);
			 return;
		 }


	 }

	 function uploadDone() {
		 if (this.readyState == 4 && this.status == 200) {
	 		document.getElementById("status").innerHTML = localisation[this.responseText];
			resetAllInput();

	 		window.setTimeout(clear,2000);

	 	}

	 }

function resetAllInput() {
	document.getElementById("fileupload").value = "";
	document.getElementById("fake_fileupload").value = "";
	inputelements = document.getElementsByTagName("input")
	for (var i=0;i<inputelements.length;i++) {
		if (inputelements[i].type == "number") {
			inputelements[i].value = 0;

		}
		inputelements[i].checked = false;

	}
}






function clear() {
	document.getElementById("status").innerHTML = "&nbsp;";
	listVideos();
}











function listVideos() {
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = listVideosDone;

	xhttp.open("GET", "/xhttp?list", true);
	console.log("Sending xhttp request to show video list");
	xhttp.send();
	console.log("Sent!");
}

function listVideosDone() {
	if (this.readyState == 4 && this.status == 200) {
		var filelist = this.responseText;
		document.getElementById("filelist").innerHTML = filelist;
	}
}

function deleteVideo(id) {
	console.log("Deleting " + id);

	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = deleteVideoDone;

	xhttp.open("GET", "/xhttp?delete=" + id, true);
	console.log("Sending xhttp request to delete video " + id);
	xhttp.send();
	console.log("Sent!");
}

function deleteVideoDone() {
	console.log("Deleted!");
	listVideos();
}
