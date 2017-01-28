#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from urlparse import urlparse,parse_qs
try:
  import simplejson as json
except (ImportError,):
  import json

histFile = open("history.txt", 'w')
PORT_NUMBER = 9000
history = []
key = "m5aorXcp0qm4vdQr309jwRJhmeAAL2009"
class WebHandler(BaseHTTPRequestHandler):

    
    def do_GET(self):
      global history
      global key
      # Parses path
      parsed = urlparse(self.path)
      page = (parsed.path)
      query = parse_qs(parsed.query)
      
      file = None
      if page == "/favicon.ico":
	file = "favicon.ico"
      elif page == "/chat/favicon.ico":
        file = "favicon.ico"
      elif page == "/":
        file = "login.html"
      elif page == "/bca2.jpg":
        file = "bca2.jpg"
      elif page == "/bca.png":
        file = "bca.png"
      elif page == "/dualboot":
        file = "dualboot.html"
      elif page == "/blair_schrank":
	file = "spam.html"
      elif page == "/blair_schrank_details":
	file = "details.html"
      elif page == "/chat/":
        if (query.get("key")[0]) == key:
          print("key recieved")
          file = "index.html"
      if file != None:
        self.send_response(200)
        #if page == "/chat":
          #print ("woohoo!")
          #if (query.get("key", [""])[0]) != key:
           # print ("key is incorrect")
          #  return
          #else:
           # self.send_header('Content-type', 'text/html')
           # self.end_headers()
           # f = open(file)
           # html = f.read()
           # self.wfile.write(html)
           # return
        
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        f = open(file)
        html = f.read()
        self.wfile.write(html)
        histFile.truncate()
        for i in history:
          histFile.write(i)
        return
        
        #history += (query.get("message", [""])[0])
        #messages = json.loads(history)
        #for i in messages:
        #  print i
        #return
      if page == "/send":
        self.send_response(200)
        string = (query.get("message", [""])[0])
        messages = json.loads(string)
        print ("I got " + messages)
        history.append(messages)
        return
    
      if page == "/fetch":
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes(json.dumps(history)))
        print ("Sending history " + json.dumps(history))
        return
      if page == "/passwd":
        self.send_response(200)
        password = (query.get("password")[0])
        print("Password Recieved! Password: " + password)
        if password == "chatPassWorD":
          print("Password is correct!")
          self.send_header("Content-type", "text/html")
          self.end_headers()
          self.wfile.write(bytes(key))
          return
        else:
          print("Password is incorrect, please try again")
    
def main():
  server = HTTPServer(('', PORT_NUMBER), WebHandler)
  try:
    print "Started httpserver on port %s" % PORT_NUMBER
    server.serve_forever()
  except Exception, ex:
    print "Caught %s" % ex
    server.socket.close()
main()
