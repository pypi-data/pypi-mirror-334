from http.server import HTTPServer, SimpleHTTPRequestHandler
from os import path

from unvibe.log import log

PORT = 8000
DIRECTORY = path.join(path.dirname(__file__), 'html')

log('Starting server on port', PORT, 'and serving files from', DIRECTORY)
httpd = HTTPServer(('localhost', PORT), SimpleHTTPRequestHandler)
httpd.serve_forever()
