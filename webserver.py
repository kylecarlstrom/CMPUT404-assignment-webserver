#  coding: utf-8 

# Copyright 2016 Tian Zhi Wang
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import SocketServer

class HttpRequest:
    def __init__(self,data):
        self._data = data
        data = data.split()
        self.command = data[0]
        self.path = data[1]

class WebServer(SocketServer.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)
        request = HttpRequest(self.data)
        if (request.command == "GET"):
            print "Serving GET" + request.path
            self.handleGET(request.path)
        else:
            #TODO Return 405
            print "Unsupported Command: " + request.command

    def handleGET(self, path):
        f = self._openfile(path)
        header = self._getHeader(200)
        self.request.sendall(header + f)
        
    def _openfile(self, path):
        if (path[-1] == '/'):
            path += "index.html"

        f = open("www" + path)
        return f.read()

    def _getHeader(self, status):
        header = "HTTP/1.1 " + str(status) + "\r\n"
        return header