
class RepositoryView {
	constructor() {
		this.repositoryList = [];
	}

	async getRepositoryList(successCallback, errorCallback) {
		let repositoryGallery = document.getElementById("repositoryGallery").children[0]

		successCallback = function (response) {
			let repositoryElement = repositoryGallery.children[0].cloneNode(true);
			let repositoryName = "Repository Name"
			let repositories = JSON.parse(response);
			repositoryGallery.innerHTML = "";
			for (let i = 0; i < repositories.length; i++) {
				let repository = repositories[i];

				repositoryElement.closest("text").innerHTML = repositoryName;
				repositoryElement.closest("a").href = "repository/" + repository;
				repositoryElement.closest(div).children[0] = new Date("DD MM YYYY");
				repositoryElement.closest(div).children[1] = repository.filesWithSATD + " SATDfiles";
				repositoryElement.closest(div).children[2] = repository.totalFiles + " files";
				
				this.repositoryList.push(repository);
				repositoryGallery.appendChild(repositoryElement);
			}
		}

		HTTPGet(getServerUrl() + "/repository", "Repository List", successCallback, errorCallback);
	}
}

class Repository {
	constructor(name, totalFiles, filesWithSATD) {
		this.name = name;
		this.totalFiles = totalFiles;
		this.filesWithSATD = filesWithSATD;
	}
}