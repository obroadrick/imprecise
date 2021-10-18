import http.client
import time
import sys

def gen_req(num_req, offset):
    req_list = ''
    for j in range(num_req):
        if j == 0:
            req_list = str((j + offset) % 5)
        else:
            req_list = req_list + ',' + str((j + offset) % 5)
    return req_list

port = 5000

connection = http.client.HTTPConnection('localhost', port)

headers = {'Content-type': 'text/html'}
num_req = int(sys.argv[2])

for i in range (int(sys.argv[1])):
    req_list = gen_req(num_req, i)
    connection.request('GET', '/' + req_list + "&0" + "&0", '', headers)
    connection.getresponse()
