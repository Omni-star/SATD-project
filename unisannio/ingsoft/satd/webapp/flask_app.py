import os.path

from flask import Flask, render_template


class SatdApp:
    def __init__(self, web_resources_directory: str):
        self.app = Flask(__name__,
                         static_folder=os.path.join(web_resources_directory, "static"),
                         template_folder=os.path.join(web_resources_directory, "templates")
                         )
        self._setup_routes()

    def _setup_routes(self):
        @self.app.route('/')
        def home():
            return render_template('index.html')

        # @self.app.route('/altra_pagina')
        # def altra_pagina():
        #     return "Questa è un'altra pagina!"

    def run(self):
        # Avvia l'app Flask
        self.app.run(debug=True)
