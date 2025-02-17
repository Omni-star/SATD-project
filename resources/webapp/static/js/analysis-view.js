import * as communicationService from './server-communication.js';

const REP_URL = communicationService.getServerUrl() 
+ "/satd/analysis"
let interval = 0;

export async function setOnPage(){
    let searchForm = document.getElementById("search-form");

    searchForm.reset();

    searchForm.onsubmit = function(event){
        event.preventDefault();
        let url = searchForm.elements[0].value;
        console.log(url);
        if (!url.startsWith("https://")) {
            url = url.replace("http://", "");
            url = "https://" + url;
        }
        startAnalysis(url);
    }

    await getAnalysisStatus();
    interval = setInterval(getAnalysisStatus, 30000);
}

export async function setAnalysisView() {
    let analysis = JSON.parse(sessionStorage.getItem("analysis"));
    
    document.querySelector("#repository-name").innerHTML = analysis.repositoryName;
    document.querySelector("#satd-number").innerHTML = analysis.satdNumber;
    document.querySelector("#satd-lines").innerHTML = analysis.totalLines;
    document.querySelector("#satd-lines").innerHTML = analysis.SATDLines.length;

    let satdLines = "";
    for (let line of analysis.SATDLines) {
        satdLines += line + "\n";
    }
    document.querySelector(".satd-textarea").innerHTML = satdLines;

    await getAnalysisStatus();
    clearInterval(interval);
    setInterval(getAnalysisStatus, 30000);
}

export async function startAnalysis(url) {    
    let successCallback = function (status, response) {
        if (status == 200) {
            console.log(response);

            clearInterval(interval);
            getAnalysisStatus();
            setInterval(getAnalysisStatus, 30000);
        }
	}

    communicationService.HTTPPost(REP_URL, JSON.stringify({url: url}), successCallback);
}

export async function getAnalysisStatus() {
    let analysisTemplate = new DOMParser().parseFromString(
		`<div class="tm-hero d-flex flex-column justify-content-center align-items-center" id="satd-analysis-container">
            <div class="spinner-border text-primary satd-spinner" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
            <div class="satd-notification">
                <span>Starting analysis...</span>
                <i class="fas fa-check"></i> <!--fa-times-->
            </div>
            <form class="d-flex tm-search-form" id="search-form">
                <input class="form-control tm-search-input" type="search" placeholder="Search" aria-label="Search">
                <button class="btn btn-outline-success tm-search-btn" type="submit">
                    <i class="fas fa-download"></i>
                </button>
            </form>
        </div>`,
		"text/html"
	).body.firstChild.children;
    let spinner = analysisTemplate[0];
    let notification = analysisTemplate[1];
    let searchForm = analysisTemplate[2];
    searchForm.reset();
    searchForm.onsubmit = function(event){
        event.preventDefault();
        let url = searchForm.elements[0].value;
        console.log(url);
        if (!url.startsWith("https://")) {
            url = url.replace("http://", "");
            url = "https://" + url;
        }
        startAnalysis(url);
    }
    let analysisContainer = document.getElementById("satd-analysis-container");
    analysisContainer.innerHTML = "";

    let successCallback = function (status, response) {
        switch (status) {
            case 200:
                analysisContainer.appendChild(notification);
                analysisContainer.appendChild(searchForm);
                notification.querySelector("span").innerText = response;
                notification.style.display = "block";
                clearInterval(interval);
                break;
            case 202:
                analysisContainer.appendChild(spinner);
                spinner.style.display = "block";
                break;
            case 500:
                analysisContainer.appendChild(notification);
                analysisContainer.appendChild(searchForm);
                notification.querySelector("span").innerText = response;
                let icon = notification.querySelector("i");
                icon.classList.remove("fa-check");
                icon.classList.add("fa-times");
                icon.style.color = "red";
                notification.style.display = "block";
                clearInterval(interval);
                break;
            case 503:
                analysisContainer.appendChild(searchForm);
                clearInterval(interval);
                break;
        }
        console.log(response);
	}

    communicationService.httpGet(REP_URL, "getAnalysisStatus", successCallback);
}