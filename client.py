import http.client
import time
port = 5000

connection = http.client.HTTPConnection('localhost', port)

headers = {'Content-type': 'text/html'}
for i in range (20):
    connection.request('GET', '/' + str(i % 5) + ",0", '', headers)
    connection.getresponse()
