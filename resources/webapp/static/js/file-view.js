import * as communicationService from './server-communication.js';

const REP_URL = communicationService.getServerUrl() 
+ "/satd/repository/"
+ sessionStorage.getItem("repositoryName")
+ "/folder/"
+ sessionStorage.getItem("satdNumber");

export async function setFileView() {
    let file = JSON.parse(sessionStorage.getItem("file"));
    
    document.querySelector("#file-name").innerHTML = file.name;
    document.querySelector("#satd-lines").innerHTML = file.totalLines;
    document.querySelector("#satd-lines").innerHTML = file.SATDLines.length;

    let satdLines = "";
    for (let line of file.SATDLines) {
        satdLines += line + "\n";
    }
    document.querySelector(".satd-textarea").innerHTML = satdLines;

}

export async function setPageTitle() {
    let pageTitle = document.getElementById("page-title");
    let repositoryName = sessionStorage.getItem("repositoryName").split("-");
    //+ "-"
    //+ new Date(repositoryName[1] * 1000).toLocaleDateString("en-GB", {day: '2-digit', month: 'long', year: 'numeric'}) 
    pageTitle.innerHTML = repositoryName[0]
    + ": "
    + sessionStorage.getItem("satdNumber")
    + " satd lines - files";
}

export async function setOnSearchForm(){
    let searchForm = document.getElementById("search-form");

    searchForm.reset();

    searchForm.onsubmit = function(event){
        event.preventDefault();
        let filter = searchForm.elements[0].value;
        getFileList(0, 8, filter);
    }
}

export async function getFileList(index = 0, size = 8, filter = "", sort = "ASC") {
    let folderTemplate = new DOMParser().parseFromString(
        `<div class="col-xl-3 col-lg-4 col-md-6 col-sm-6 col-12 mb-5">
            <a>
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 420 236" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="satd-file">
                    <path d="M200 20H150a20 20 0 0 0-20 20v156a20 20 0 0 0 20 20h120a20 20 0 0 0 20-20V80z"></path>
                    <polyline points="200 20 200 80 290 80"></polyline>
                    <line x1="150" y1="86" x2="180" y2="86"></line>
                    <line x1="150" y1="126" x2="270" y2="126"></line>
                    <line x1="150" y1="166" x2="270" y2="166"></line>
                </svg>
            </a>
            <div class="d-flex justify-content-between">
                <span style="font-size: 1em">18 Oct 2020</span>
                <span style="font-size: 1em">9,906 files</span>
            </div>
        </div>`,
        "text/html"
    ).body.firstChild;
    let fileGallery = document.getElementById("repositoryGallery")

    let successCallback = function (status, response) {
        if (status == 200) {
            let pagedFiles = JSON.parse(response);
            let maxSatdNumber = Number(sessionStorage.getItem("satdNumber"));
            console.log(pagedFiles);
            fileGallery.innerHTML = "";
            for (let i = 0; i < pagedFiles.content.length; i++) {
                let fileElement = folderTemplate.cloneNode(true);
                fileGallery.appendChild(fileElement);
                let file = pagedFiles.content[i];

                fileElement.querySelector("a").onclick = function(){
                    sessionStorage.setItem("file", JSON.stringify(file));
                    sessionStorage.setItem("pageIndex", 0);
                    window.location.href = "file-detail.html";
                }
                // fileElement.querySelector(".satd-file-title").innerHTML = file.name + "askdkaskdmkasmskmdsakmkmk";
                // fileElement.querySelector(".satd-file-description").innerHTML = file.totalLines + " total lines";

                let h = (1 - maxSatdNumber / file.totalLines) * 100;
                // if (h < 1){
                //     h = (1 - h) * 100;
                // }
                console.log("H: " + h);
                let s = 100; //Math.floor(Math.random() * 255);
                let l = 50;
                fileElement.querySelector(".satd-file").style.backgroundColor = "hsl(" + h + "," + s + "%," + l + "%)";

                let folderDescription = fileElement.querySelector("div");
                folderDescription.children[0].innerHTML = file.name;
                folderDescription.children[1].innerHTML = file.totalLines + " lines";
            }
            sessionStorage.setItem("pageIndex", pagedFiles.pageIndex);
            sessionStorage.setItem("totalPages", pagedFiles.totalPages);

            managePagination(size, filter);
        }
    }

    communicationService.httpGet(
        (
            REP_URL +
            "?index=" + index + 
            "&size=" + size + 
            "&filter=" + filter + 
            "&sort=" + sort
        ),
        "Repository List", 
        successCallback
    );
}

async function managePagination(size=8, filter="") {

    let pageIndex = parseInt(sessionStorage.getItem("pageIndex"));
    let totalPages = sessionStorage.getItem("totalPages");
    console.log("Total pages: " + totalPages);

    let currentPageText = document.querySelector("#current-page-text");
    let totalPagesText = document.querySelector("#total-pages-text");

    currentPageText.innerHTML = pageIndex+1;
    totalPagesText.innerHTML = "of " + totalPages;

    let prevPageButton = document.querySelector("#prev-page");

    if (pageIndex > 0) {
        prevPageButton.classList.remove("disabled");
        prevPageButton.onclick = function(){
            console.log("Page index selected: " + (pageIndex-1));
            getFileList(pageIndex-1, size, filter);
        };
    }else{
        prevPageButton.classList.add("disabled");
        prevPageButton.onclick = function(){
            console.log("Prev page button disabled");
        };
    }

    let nextPageButton = document.querySelector("#next-page");

    if (pageIndex < totalPages-1) {
        nextPageButton.classList.remove("disabled");
        nextPageButton.onclick = function(){
            console.log("Page index selected: " + (pageIndex+1));
            getFileList(pageIndex+1, size, filter);
        };
    }else{
        nextPageButton.classList.add("disabled");
        nextPageButton.onclick = function(){
            console.log("Next page button disabled");
        };
    }

    let pageNumbersGroup = document.querySelector("#page-numbers");

    let pageNumber = pageNumbersGroup.children[0].cloneNode(true);
    pageNumber.classList.remove("active");

    pageNumbersGroup.innerHTML = "";
    if (totalPages > 7) {
        pageNumbersGroup.appendChild(
            createPageButton(pageNumber, 1, 0, size, filter)
        );

        let startPage = 3;
        let endPage = 5;
        if (pageIndex > 3) {
            if (pageIndex > totalPages-5) {
                startPage = totalPages-4;
                endPage = totalPages-1;
            }else{
                startPage = pageIndex;
                endPage = pageIndex+2;
            }

            pageNumbersGroup.appendChild(
                createPageButton(pageNumber, "...", startPage-2, size, filter)
            );
        }else{
            pageNumbersGroup.appendChild(
                createPageButton(pageNumber, 2, 1, size, filter)
            );
        }

        for (let i = startPage; i <= endPage; i++) {
            pageNumbersGroup.appendChild(
                createPageButton(pageNumber, i, i-1, size, filter)
            );
        }

        if (pageNumbersGroup.children.length < 6) {
            pageNumbersGroup.appendChild(
                createPageButton(pageNumber, "...", endPage, size, filter)
            );
        }

        pageNumbersGroup.appendChild(
            createPageButton(pageNumber, totalPages, totalPages-1, size, filter)
        );

        if (pageIndex < 3) {
            pageNumbersGroup.children[pageIndex].classList.add("active");
        }else if(pageIndex <= totalPages-4){
            pageNumbersGroup.children[3].classList.add("active");
        }else{
            pageNumbersGroup.children[7 - (totalPages-pageIndex)].classList.add("active");
        }
    }else{
        for (let i = 1; i <= totalPages; i++) {
            pageNumbersGroup.appendChild(
                createPageButton(pageNumber, i, i-1, size, filter)
            );
        }

        pageNumbersGroup.children[pageIndex].classList.add("active");
    }
}

function createPageButton(buttonTemplate, innerHtml, index, size=8, filter="") {
    let button = buttonTemplate.cloneNode(true);
    button.innerHTML = innerHtml;
    button.onclick = function(){
        console.log("Page index selected: " + index);
        getFileList(index, size, filter);
    }

    return button;
}