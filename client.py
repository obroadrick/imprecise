import http.client
import time
import sys
port = 5000

connection = http.client.HTTPConnection('localhost', port)

headers = {'Content-type': 'text/html'}
for i in range (int(sys.argv[1])):
    connection.request('GET', '/' + str(i % 5) + ",0", '', headers)
    connection.getresponse()
