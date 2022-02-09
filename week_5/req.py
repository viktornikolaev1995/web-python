import base64
import requests
from json import loads
from requests.auth import HTTPBasicAuth


string = "aladdin:opensesame"
result = base64.b64encode(bytes(string, 'utf-8'))

print(result)

request = requests.post(
    'https://datasend.webpython.graders.eldf.ru/submissions/1/',
    headers={'Authorization': 'Basic YWxsYWRpbjpvcGVuc2VzYW1l'}
)

print(request.status_code)
print(request.text)

instructions = loads(request.text)
print(instructions, type(instructions))
print(type(request.text))

login = instructions['login']
password = instructions['password']
path = 'https://datasend.webpython.graders.eldf.ru/'+instructions['path']

string = f'{login}:{password}'
credentials = base64.b64encode(bytes(string, 'utf-8'))

print(credentials)
print(path)

answer = requests.put(path, auth=HTTPBasicAuth(login, password))

print(answer.status_code)
print(answer.text)
