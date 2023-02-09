#!/usr/bin/env python3
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
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

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib.parse

def help():
    print("httpclient.py [GET/POST] [URL]\n")

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    def get_host_port(self,url):
        """
        Port getter from the url
        Hostname getter from the url
        Path getter from the url
        """
        parse_result = urllib.parse.urlparse(url)
        port = parse_result.port if parse_result.port else 80 # port 80 by default
        host_name = parse_result.hostname 
        path = parse_result.path if parse_result.path != "" else "/" 
        if host_name is None: 
            if path.find("/") < 0: # if cannot locate a single '/' 
                path += "/"
            temp_index = path.find("/")
            host_name = path[0 : temp_index]
            path = path[temp_index: ]      
        return port, host_name, path

    def connect(self, host, port):
        """"
        Connect to the webserver via provided host and port
        """
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        return None

    def get_code(self, data):
        """
        Response code getter 
        """
        parse_data = data.split("\r\n\r\n")
        response_code = parse_data[0].split('\r\n')[0].split()[1]
        response_code = int(response_code)
        # response_code = data.split()[1]
        # response_code = int(response_code) # cast from str to int type 
        return response_code

    def get_headers(self,data):
        """
        Headers getter by using response 
        """
        parse_data = data.split("\r\n\r\n")
        headers = parse_data[0]
        return headers
    
    def get_body(self, data):
        """
        Body content getter
        """
        parse_data = data.split("\r\n\r\n")
        body_content = parse_data[1]
        return body_content
    
    def sendall(self, data):
        """
        Send the client message(request) to the webserver
        """
        self.socket.sendall(data.encode('utf-8'))
        
    def close(self):
        self.socket.close()

    # read everything from the socket(webserver)
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024) # receive 1024 bytes from webserver response
            if (part):
                buffer.extend(part) # store the recieved part
            else: # part == None
                done = not part
        return buffer.decode('utf-8')

    def GET(self, url, args=None):
        port, host_name, path = self.get_host_port(url)
        if args != None:
            query_parameters = urllib.parse.urlencode(args)
            path += "?"
            path += query_parameters
        request = f"GET {path} HTTP/1.0\r\nHost: {host_name}\r\n\r\n" # Client message
        self.connect(host_name, port)
            
        self.sendall(request)
        data = self.recvall(self.socket)
        self.close()
        # print(data)
        response_code = self.get_code(data)
        body_content = self.get_body(data)
            
        return HTTPResponse(response_code, body_content)

    def POST(self, url, args=None):
        
        port, host_name, path = self.get_host_port(url)
        request = f"POST {path} HTTP/1.0\r\nHost: {host_name}\r\n" # Client messages
        self.connect(host_name, port)
            
        if args != None:
            extended_request = urllib.parse.urlencode(args)
            extra_content_type = "application/x-www-form-urlencoded"
            request += f"Content-Type: {extra_content_type}\r\n"
            content_length = len(extended_request)
            request += f"Content-Length: {content_length}\r\n\r\n"
            request += extended_request
        else: 
            request += f"Content-Type: application/octet-stream\r\n" 
            request += f"Content-Length: 0\r\n"
            request += "\r\n"
            
        self.sendall(request)
        data = self.recvall(self.socket)
        self.close()
        # print(data)
        response_code = self.get_code(data)
        body_content = self.get_body(data)
        return HTTPResponse(response_code, body_content)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else: # command == "GET"
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    # print(sys.argv) # argv ['httpclient.py', '[GET]', '[http://www.google.com]']
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        http_response = client.command( sys.argv[2], sys.argv[1] )
        print(http_response.code)
        print(http_response.body)
    else:
        print(client.command( sys.argv[1] ))
