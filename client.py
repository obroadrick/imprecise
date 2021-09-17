import http.client

port = 8000

connection = http.client.HTTPConnection('localhost', port)

headers = {'Content-type': 'text/html'}
for i in range (5):
    connection.request('GET', '/', '', headers)
    response = connection.getresponse()
    print(response.read().decode())
