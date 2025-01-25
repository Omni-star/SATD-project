import os.path
from math import ceil

from flask import Flask, render_template, request, make_response

from .file_service import FileService
from .repository_service import RepositoryService
from ..git.analysis_status import AnalysisStatus


class SatdApp:
  def __init__(self, config: dict):
    self.app = Flask(__name__,
                     static_folder=os.path.join(config["webapp_res_directory"], "static"),
                     template_folder=os.path.join(config["webapp_res_directory"], "templates")
                     )

    self.repository_service = RepositoryService(config["data_directory"])
    self.files_service = FileService(config["data_directory"])
    self.config = config
    self._setup_routes()

  def _setup_routes(self):
    @self.app.route('/')
    def home():
      return render_template('index.html')
    
    @self.app.route('/<page_name>')
    def navigate(page_name: str = 'index.html'):
      return render_template(page_name)

    @self.app.route('/satd/repository', methods=['GET', 'POST'])
    def get_repositories():
      if request.method == 'GET':
        page_index = request.args.get('index', type=int, default=0)
        page_size = request.args.get('size', type=int, default=10)
        filter = request.args.get('filter', type=str, default="")
        order = request.args.get('order', type=str, default="ASC")

        return self.repository_service.get_paged_repositories(
            page_index, page_size, filter, order
            )
      elif request.method == 'POST':
        repository = request.get_json()
        
        if self.repository_service.save_repository(repository):
          return self.app.make_response((
            "Repository saved successfully!",
            200
          ))
        else:
          return self.app.make_response((
            "Repository saving failed!",
            500
          ))
      else:
        return self.app.make_response((
          "Method not allowed!",
          405
        ))

    @self.app.route('/satd/repository/<repository_name>/folder')
    def get_folders(repository_name: str):
      page_index = request.args.get('index', type=int, default=0)
      page_size = request.args.get('size', type=int, default=10)
      order = request.args.get('order', type=str, default="ASC")

      return self.files_service.get_folders(
        repository_name, page_index, page_size, order
      )

    @self.app.route('/satd/repository/<repository_name>/folder/<satd_number>')
    def get_files(repository_name: str, satd_number: int):
      page_index = request.args.get('index', type=int, default=0)
      page_size = request.args.get('size', type=int, default=10)
      filter = request.args.get('filter', type=str, default="")
      order = request.args.get('order', type=str, default="ASC")

      return self.files_service.get_files(
        repository_name, satd_number, page_index, page_size, filter, order
      )

    @self.app.route('/satd/analysis', methods=['GET', 'POST'])
    def satd_analysis():
      if request.method == 'GET':
        analysis_status: AnalysisStatus = self.repository_service.get_analysis_status()
        if analysis_status == AnalysisStatus.IN_PROGRESS:
          return self.app.make_response(
            "Repository analysis in progress...",
            202
          )
        elif analysis_status == AnalysisStatus.DONE:
          return self.app.make_response(
            "Repository analysis successfully completed.",
            200
          )
        elif analysis_status == AnalysisStatus.ERROR:
          return self.app.make_response(
            "Repository analysis error: repository not found.",
            500
          )
        elif analysis_status == AnalysisStatus.NOT_STARTED:
          return self.app.make_response(
            "Repository analysis has not started yet.",
            503
          )
      elif request.method == 'POST':
        repository = request.get_json()

        self.repository_service.start_repository_analysis(
          repository['url'],
          self.config['clone_repos_directory'],
          self.config['file_type_to_analyse'],
          self.config['satd_keywords'],
          self.config['data_directory']
        )
      else:
        return self.app.make_response((
          "Method not allowed!",
          405
        ))

    @self.app.route('/satd/test')
    def get_test():
      return str(ceil(44 / 6))
      

    # @self.app.route('/altra_pagina')
    # def altra_pagina():
    #     return "Questa è un'altra pagina!"

  def run(self):
    # Avvia l'app Flask
    self.app.run(debug=True)
