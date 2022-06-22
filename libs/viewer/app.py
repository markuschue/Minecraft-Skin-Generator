# Python script that runs a local server that allows the user to view the generated skins.

import http.server
import socketserver

PORT = 8080

def run():
  Handler = http.server.SimpleHTTPRequestHandler

  Handler.extensions_map = {
    '.manifest': 'text/cache-manifest',
    '.html': 'text/html',
    '.png': 'image/png',
    '.jpg': 'image/jpg',
    '.svg':	'image/svg+xml',
    '.css':	'text/css',
    '.bundle.js':	'application/x-javascript',
    '.js':	'application/x-javascript',
    '': 'application/octet-stream', # Default
  }

  httpd = socketserver.TCPServer(("", PORT), Handler)

  print("Serving at port", PORT)
  httpd.serve_forever()

if __name__ == '__main__':
  run()