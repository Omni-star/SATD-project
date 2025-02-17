import * as communicationService from './server-communication.js';

const REP_URL = communicationService.getServerUrl() 
+ "/satd/repository/"
+ sessionStorage.getItem("repositoryName")
+ "/folder";

export async function setPageTitle() {
    let pageTitle = document.getElementById("page-title");
    let repositoryName = sessionStorage.getItem("repositoryName").split(":");
    //+ "-"
    //+ new Date(repositoryName[1] * 1000).toLocaleDateString("en-GB", {day: '2-digit', month: 'long', year: 'numeric'}) 
    pageTitle.innerHTML = repositoryName[0]
    + " - folders grouped by SATD";
}

export async function getFolderList(index = 0, size = 8, order = "DESC") {
    let folderTemplate = new DOMParser().parseFromString(
        `<div class="col-xl-3 col-lg-4 col-md-6 col-sm-6 col-12 mb-5">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 420 236" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="satd-folder">
                <a>
                    <path d="M420 216a20 20 0 0 1-20 20H20a20 20 0 0 1-20-20V20a20 20 0 0 1 20-20h126l40 40H400a20 20 0 0 1 20 20z"></path>
                    <text x="210" y="148" text-anchor="middle" class="satd-svg-title text-wrap">OpenFGA</text>
                    <text x="210" y="198" text-anchor="middle" class="satd-svg-description text-wrap">8,906 SATDfiles</text>
                </a>
            </svg>
            <div class="d-flex justify-content-between tm-text-gray">
                <span class="tm-text-gray-light">18 Oct 2020</span>
                <span>9,906 files</span>
            </div>
        </div>`,
        "text/html"
    ).body.firstChild;
    let folderGallery = document.getElementById("repositoryGallery")

    let successCallback = function (status, response) {
        if (status == 200) {
            let pagedfolder = JSON.parse(response);
            let maxSatdNumber = 0;
            console.log(pagedfolder);
            folderGallery.innerHTML = "";
            for (let i = 0; i < pagedfolder.content.length; i++) {
                let folderElement = folderTemplate.cloneNode(true);
                folderGallery.appendChild(folderElement);
                let folder = pagedfolder.content[i];

                folderElement.querySelector("a").onclick = function(){
                    sessionStorage.setItem("pageIndex", 0);
                    sessionStorage.setItem("satdNumber", folder.satdNumber);
                    window.location.href = "folder-detail.html";
                }

                folder.satdNumber = folder.satdNumber == null ? 0 : Number(folder.satdNumber);

                if (maxSatdNumber < folder.satdNumber) {
                    maxSatdNumber = folder.satdNumber;
                    console.log("Max satd number: " + maxSatdNumber);
                }
                let h = (1 - folder.satdNumber/ maxSatdNumber) * 100;
                let s = 100; //Math.floor(Math.random() * 255);
                // console.log("G: " + g);
                let l = 50;
                folderElement.querySelector(".satd-folder path").style.fill = "hsl(" + h + "," + s + "%," + l + "%)";
                folderElement.querySelector(".satd-svg-title").innerHTML = folder.satdNumber + " SATD lines";
                folderElement.querySelector(".satd-svg-description").innerHTML = "for each file";

                let folderDescription = folderElement.querySelector("div");
                folderDescription.children[0].innerHTML = ""
                folderDescription.children[1].innerHTML = folder.files + " files";
            }
            sessionStorage.setItem("pageIndex", pagedfolder.pageIndex);
            sessionStorage.setItem("totalPages", pagedfolder.totalPages);

            managePagination(size);
        }
    }

    communicationService.httpGet(
        (
            REP_URL +
            "?index=" + index + 
            "&size=" + size + 
            "&order=" + order
        ),
        "Repository List", 
        successCallback
    );
}

async function managePagination(size=8) {

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
            getFolderList(pageIndex-1, size);
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
            getFolderList(pageIndex+1, size);
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
            createPageButton(pageNumber, 1, 0, size)
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
                createPageButton(pageNumber, "...", startPage-2, size)
            );
        }else{
            pageNumbersGroup.appendChild(
                createPageButton(pageNumber, 2, 1, size)
            );
        }

        for (let i = startPage; i <= endPage; i++) {
            pageNumbersGroup.appendChild(
                createPageButton(pageNumber, i, i-1, size)
            );
        }

        if (pageNumbersGroup.children.length < 6) {
            pageNumbersGroup.appendChild(
                createPageButton(pageNumber, "...", endPage, size)
            );
        }

        pageNumbersGroup.appendChild(
            createPageButton(pageNumber, totalPages, totalPages-1, size)
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
                createPageButton(pageNumber, i, i-1, size)
            );
        }

        pageNumbersGroup.children[pageIndex].classList.add("active");
    }
}

function createPageButton(buttonTemplate, innerHtml, index, size=8) {
    let button = buttonTemplate.cloneNode(true);
    button.innerHTML = innerHtml;
    button.onclick = function(){
        console.log("Page index selected: " + index);
        getFolderList(index, size);
    }

    return button;
}