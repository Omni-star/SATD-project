import * as communicationService from './server-communication.js';

const REP_URL = communicationService.getServerUrl() + "/satd/repository";

export async function setOnPageSelected(){
	let searchForm = document.getElementById("search-form");

	searchForm.reset();

	searchForm.onsubmit = function(event){
		event.preventDefault();
		let filter = searchForm.elements[0].value;
		getRepositoryList(0, 8, filter);
	}
}

export async function getRepositoryList(index = 0, size = 8, filter = "", sort = "ASC") {
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
	let repositoryGallery = document.getElementById("repositoryGallery")

	let successCallback = function (status, response) {

		if (status == 200) {
			let pagedRepositories = JSON.parse(response);
			console.log(pagedRepositories);
			repositoryGallery.innerHTML = "";
			for (let i = 0; i < pagedRepositories.content.length; i++) {
				let repositoryElement = folderTemplate.cloneNode(true);
				repositoryGallery.appendChild(repositoryElement);
				let repository = pagedRepositories.content[i];

				repositoryElement.querySelector("a").onclick = function(){
					sessionStorage.setItem("repositoryName", repository.name + ":" + repository.creationDate);
					sessionStorage.setItem("pageIndex", "0");
					window.location.href = "repository-detail.html";
				}
				repositoryElement.querySelector(".satd-svg-title").innerHTML = repository.name;
				repositoryElement.querySelector(".satd-svg-description").innerHTML = repository.filesWithSATD + " SATD files";

				let folderDescription = repositoryElement.querySelector("div");
				folderDescription.children[0].innerHTML = new Date(
					repository.creationDate * 1000).toLocaleDateString('en-GB',
					{day: 'numeric', month: 'long', year: 'numeric'}
				);
				folderDescription.children[1].innerHTML = repository.totalFiles + " files";
			}
			sessionStorage.setItem("pageIndex", pagedRepositories.pageIndex);
			sessionStorage.setItem("totalPages", pagedRepositories.totalPages);

			managePagination(size, filter);
		}
	}

	let errorCallback = function (response) {
		alert("Error while fetching repository list");
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
			getRepositoryList(pageIndex-1, size, filter);
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
			getRepositoryList(pageIndex+1, size, filter);
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
		getRepositoryList(index, size, filter);
	}

	return button;
}