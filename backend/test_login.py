import urllib.request, json
data = json.dumps({'email': 'test7@gmail.com', 'password': 'testpassword123'}).encode('utf-8')
req = urllib.request.Request('http://localhost:8000/api/auth/login/', data=data, headers={'Content-Type': 'application/json'})
try:
    print(urllib.request.urlopen(req).read())
except Exception as e:
    print(e.read())
