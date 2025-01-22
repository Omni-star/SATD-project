import os.path
from math import ceil

from flask import Flask, render_template, request, make_response
from .repository_service import RepositoryService


class SatdApp:
  def __init__(self, data_directory: str, web_resources_directory: str):
    self.app = Flask(__name__,
                     static_folder=os.path.join(web_resources_directory, "static"),
                     template_folder=os.path.join(web_resources_directory, "templates")
                     )

    self.repository_service = RepositoryService(data_directory)
    self.files_service = RepositoryService(data_directory)
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

    @self.app.route('/satd/test')
    def get_test():
      return str(ceil(44 / 6))
      

    # @self.app.route('/altra_pagina')
    # def altra_pagina():
    #     return "Questa è un'altra pagina!"

  def run(self):
    # Avvia l'app Flask
    self.app.run(debug=True)
