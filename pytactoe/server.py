from sockerserver import TCPServer, BaseRequestHandler

class MyTCPHandler(BaseRequestHandler):
  def handle(self):
        data = self.request.recv().strip()
        print("{} wrote:".format(self.client_address[0]))
        print(data)
        self.request.sendall(self.data.upper())


def serve(port, host=''):
    with TCPServer((host, port), MyTCPHandler) as s:
        s.serve_forever()
