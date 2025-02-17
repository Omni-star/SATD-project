
export function getServerUrl() {
	let serverUrl = location.protocol +
		"//" + location.hostname +
		":" + location.port;

	return serverUrl;
}

//================= Methods: HTTP_POST
export function HTTPPost(url, jsonBodyString, callback) {
	//event.preventDefault();

	let request = new XMLHttpRequest();   // new HttpRequest instance

	request.open("POST", url, true);
	request.setRequestHeader("content-type", "application/json");

	// request.onerror = function () {
	// 	alert.log("** An error occurred during the transaction");
	// };
	//	request.send(JSON.stringify(jsonBodyString));
	request.send(jsonBodyString);
	request.onreadystatechange = function () {
		if (this.readyState === 4) {
			callback(this.status, this.responseText);
		}
	};
}

//================= Methods: HTTP_GET
export function httpGet(url, message, callback) {

	let request = new XMLHttpRequest();   // new HttpRequest instance

	request.open("GET", url, true);
	request.setRequestHeader("content-type", "application/json");

	request.send();
	request.onreadystatechange = function () {
		if (this.readyState === 4) {
			console.log(message);
			callback(this.status, this.responseText);
		}
	};
}


//================= Methods: HTTP_PUT
function HTTPPut(url, jsonBodyString, message) {
	let request = new XMLHttpRequest();   // new HttpRequest instance

	request.open("PUT", url, true);
	request.onerror = function () {
		alert.log("** An error occurred during the transaction");
	};

	request.send(jsonBodyString);
	request.onreadystatechange = function () {
		if (this.readyState === 4) {
			if (this.status === 500) {
				let results = JSON.parse(this.responseText);
				alert("error" + this.responseText);
			} else if (this.status === 200) {
				alert(message);
			}
		}
	};
}

//================= Methods: HTTP_DELETE
function HTTPDelete(url, token, mex) {
	let xhr = new XMLHttpRequest();
	xhr.open("DELETE", url, true);
	xhr.setRequestHeader('Authorization', 'Bearer ' + token);

	xhr.onload = function () { };



	xhr.send(null);
	alert(mex);
};

//================= Methods: HTTP_PATCH
function HTTPPatch(url, token, jsonBodyString, mex) {
	event.preventDefault();
	let request = new XMLHttpRequest();   // new HttpRequest instance

	request.open("PATCH", url, true);
	request.setRequestHeader('Authorization', 'Bearer ' + token);
	request.setRequestHeader("content-type", "application/json");

	request.onerror = function () {
		alert.log("** An error occurred during the transaction");
	};
	request.send(jsonBodyString);
	request.onreadystatechange = function () {
		if (this.readyState === 4) {
			console.log("Request: token " + token + " jsonBody: " + jsonBodyString);
			console.log("Response: " + this.responseText);
			let results = JSON.parse(this.responseText);

			if (this.status === 500) {
				alert("error" + this.responseText);
			} else if (this.status === 200) {
				alert(mex);
			}
		}
	};
}