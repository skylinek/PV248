import sys
import urllib.parse as urlibparser
import urllib.request as urlibrequest
import urllib.error as urliberror
import http.server as myHTTP
import os
import socketserver


class Server(socketserver.ThreadingMixIn, myHTTP.HTTPServer):
    pass


def wrap_handler(dir):
    class RequestHandler(myHTTP.CGIHTTPRequestHandler):
       def myFunction(self):
            actualDir = os.path.dirname(self.path)
            if actualDir not in self.cgi_directories:
                self.cgi_directories.append(actualDir)
                res_dir = urlibparser.urlparse(self.path[1:])
            if  os.path.isdir(res_dir):
                self.send_response(403)
                self.send_header('Connection', 'close')
                self.end_headers()
                self.wfile.write(bytes('', 'utf-8'))
            elif os.path.isfile(res_dir):
                if urlibparser.urlparse(self.path).path[1:].endswith('.cgi'):
                    if not self.is_cgi():
                        MYfile = myHTTP.SimpleHTTPRequestHandler.send_head(self)
                        if MYfile:
                            try:
                                self.copyfile(MYfile, self.wfile)
                            finally:
                                MYfile.close()
                    else:
                        self.run_cgi()
                else:
                    with myHTTP.SimpleHTTPRequestHandler.send_head(self) as MYfile:
                        if MYfile:
                            self.copyfile(MYfile, self.wfile)
                        else:
                            MYfile.close()
            else:
                self.send_response(404)
                self.send_header('Connection', 'close')
                self.end_headers()
                self.wfile.write(bytes('', 'utf-8'))

       def do_GET(self):
           self.myFunction()

       def do_POST(self):
           self.myFunction()

       def do_HEAD(self):
           self.myFunction()


    return RequestHandler


def main():
    port = int(sys.argv[1])
    dir = sys.argv[2]
    os.chdir(os.path.realpath(dir))
    httpd = Server(('localhost', port), wrap_handler(dir))
    httpd.serve_forever()


if __name__ == '__main__':
    main()