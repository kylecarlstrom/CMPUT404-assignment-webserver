#  coding: utf-8 

# Copyright 2016 Tian Zhi Wang, Kyle Carlstrom
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

import SocketServer, os, mimetypes

class HttpRequest:
    def __init__(self,data):
        self._data = data
        data = data.split()
        self.command = data[0]
        self.path = "www" + data[1]

class WebServer(SocketServer.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print("Got a request of: %s\n" % self.data)

        request = HttpRequest(self.data)

        if request.command != "GET":
            # Return 405
            self.sendError(405)
        elif not self.isPathContained(request.path):
            # Return 404
            self.sendError(404)
        else:
            # Handle get
            self.handleGet(request.path)

    def isPathDirectory(self, path):
        return os.path.isdir(path)

    def doesFileExist(self, path):
        return os.path.isfile(path)

    def openFile(self, path):
        f = open(path)
        return f.read()

    # If the path is contained, the path should start with where we currently are plus the www directory
    def isPathContained(self, path):
        return os.path.realpath(path).startswith(os.getcwd() + "/www")

    def handleGet(self, path):
        if self.isPathDirectory(path):
            path += "/index.html"

        if self.doesFileExist(path):
            self.sendResponse(path)
        else:
            # Return 404
            self.sendError(404)

    def sendResponse(self, path):
        header = self._getHeader(200)
        f = self.openFile(path)
        contentType = mimetypes.guess_type(path)[0]
        contentHeader = "Content-type: " + contentType + ";\r\n\r\n"
        self.request.sendall(header + contentHeader + f)

    def sendError(self, status):
        self.request.sendall(self._getHeader(status))

    def _getHeader(self, status):
        header = "HTTP/1.1 " + str(status) + "\r\n"
        return header
