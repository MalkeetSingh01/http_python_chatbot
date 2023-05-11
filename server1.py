from http.server import HTTPServer, BaseHTTPRequestHandler
import time
from urllib.parse import urlparse, parse_qs

import json

HOST="127.0.0.1"

PORT=8000

messageList={}

# cached_message

class CustomConnection(BaseHTTPRequestHandler):
    def do_GET(self):
        query = urlparse(self.path).query
        data= parse_qs(query)
        print(data)
        # print(self.path)
        path = urlparse(self.path).path
        print(path)
        if(path=="/message"):
            self.send_response(200)
            self.send_header("Content-Type","text/html")
            self.end_headers()
            key_hash=str(data['param2'][0].lower()+"%"+data['param1'][0].lower())
            # type(key_hash)
            # print(str(messageList[key_hash][-1]))
            if key_hash in messageList and messageList[key_hash]:
                self.wfile.write(bytes(str(messageList.get(key_hash)[-1]),"utf-8"))
            else :self.wfile.write(bytes("","utf-8"))
        else:
            self.send_response(400)
            self.send_header("Content-Type","text/html")
            self.end_headers()
            self.wfile.write(bytes("Invalid path","utf-8"))
         
    def do_POST(self):
        length_int=int(self.headers['Content-Length'])
        body=self.rfile.read(length_int)
        data=json.loads(body.decode('utf-8'))
        key_hash=data['user'].lower()+"%"+data['friend'].lower()
        # messageList[key_hash]=[*messageList[key_hash],data['message']]
        # sorted_keyHash = ''.join(sorted(key_hash))
        # if sorted_keyHash in messageList:
        #    messageList[sorted_keyHash].append(data['message'])
        # else:
        #    messageList[sorted_keyHash] = [data['message']]
        if key_hash in messageList:
           messageList[key_hash].append(data['message'])
        else:
           messageList[key_hash] = [data['message']]
        # print(messageList)
        self.send_response(200)
        self.send_header("Content-Type","application/json")
        self.end_headers()
        self.wfile.write(bytes("Message sent...I think","utf-8"))

if __name__ == '__main__':
    server=HTTPServer((HOST,PORT),CustomConnection)
    print('server3 started')
    server.serve_forever()