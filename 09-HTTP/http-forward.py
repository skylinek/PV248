import sys
import http.server
import http.client
import socket
import json
from http.client import HTTPConnection
from urllib import request



def addHTTP(adress):
    if "http://" in adress:
        return adress
    else:
        return "http://" + adress

port = sys.argv[1]
forwardTO = sys.argv[2]
forwardTO=addHTTP(forwardTO)

def testValidJson(JSON):
    try:
        myJSON=json.loads(JSON)
    except ValueError:
        return False
    return True


class myServer(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        timeout=int(1)
        jsonResult = dict()
        try:
            with request.urlopen(forwardTO, timeout=timeout) as client:
                myResponse=client


                jsonResult["code"] = myResponse.getcode()
                jsonResult["headers"] = dict(myResponse.getheaders())
                contentType=  myResponse.info().get_content_type()
                myBody=str(myResponse.read())

                if contentType== "application/json" or testValidJson(myBody):
                    jsonResult["json"]=myBody
                else:
                    jsonResult["content"]=myBody
        except timeout:
            jsonResult["code"]="timeout"

        self.send_response(200)

        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(bytes(json.dumps(jsonResult).encode()))
        return

    def do_POST(self):
        MYrequest = self.rfile.read( int(self.headers.get('content-length', 0)))
        isJSON=testValidJson(MYrequest)
        if isJSON is not True:
            self.send_response(200)
            myDict={"code": "invalid json"}
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(bytes(json.dumps(myDict),encoding='utf8'))
            return
        myJSON= json.loads(MYrequest)
        myHeaders=dict()
        if "headers" in myJSON.keys():
            myHeaders = myJSON["headers"]

        if ("type" in myJSON and "content" not in myJSON and myJSON["type"] == "POST"):
            self.send_response(200)
            myDict = {"code": "invalid json"}
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(bytes(json.dumps(myDict).encode()))
            return
        elif ("url" not in myJSON):
            self.send_response(200)
            myDict = {"code": "invalid json"}
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(bytes(json.dumps(myDict).encode()))
            return


        myBody=None
        if "type" in myJSON:
            if  myJSON["type"] == "POST":
                myBody = myJSON["content"]
        else:
            myJSON["type"] = "GET"



        mynewURL=addHTTP(myJSON["url"])
        mynewURL=myJSON["url"]
        zbytekURL=""

        if "//" in myJSON["url"]:
            mySplittedURL=myJSON["url"].split("/", 3)
            mynewURL= mySplittedURL[2]
            if len(mySplittedURL)>3:
                zbytekURL= "/"+mySplittedURL[3]
        elif "/" not in myJSON["url"] :
            pass
        else:
            mySplittedURL=myJSON["url"].split("/", 1)
            mynewURL= mySplittedURL[0]
            zbytekURL= "/"+mySplittedURL[1]


        if "timeout" in myJSON:
            myClient=HTTPConnection(mynewURL, timeout=myJSON["timeout"])
        else:
            myClient=HTTPConnection(mynewURL, timeout=1)
        try:
            myClient.request(myJSON["type"], zbytekURL, myBody, myHeaders)
        except socket.timeout:
            jsonResult = {}
            jsonResult["code"] = "timeout"
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(bytes(json.dumps(jsonResult).encode()))
            return

        self.send_response(200)
        myResponse=myClient.getresponse()
        jsonResult = {}
        jsonResult["code"] = myResponse.getcode()
        jsonResult["headers"] = dict(myResponse.getheaders())
        contentType = myResponse.info().get_content_type()
        myBody = str(myResponse.read())

        if contentType == "application/json" or testValidJson(myBody):
            jsonResult["json"] = myBody
        else:
            jsonResult["content"] = myBody

        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(bytes(json.dumps(jsonResult).encode()))




def main():


    try:
        server = http.server.HTTPServer(('127.0.0.1', int(port)), myServer)
        server.serve_forever()

    except KeyboardInterrupt:
        server.socket.close()



if __name__ == '__main__':
    main()