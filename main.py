####################################################################################################

from wsgiref.simple_server import make_server
from pyramid.config import Configurator

SERVER_PORT = 8080

####################################################################################################

if __name__ == "__main__":
    with Configurator() as config:
        config.add_route("home", "/")
        config.add_route("ocr", "/ocr")
        config.add_static_view(name="data", path="static")
        config.include("pyramid_chameleon")
        config.scan("views")
        app = config.make_wsgi_app()

    server = make_server("0.0.0.0", SERVER_PORT, app)
    server.serve_forever()

####################################################################################################