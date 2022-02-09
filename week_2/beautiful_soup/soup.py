html = """<!DOCTYPE html>
<html lang="en">
<head>
<title>test page</title>
</head>
<body class="mybody" id="js-body">
<p class="text odd">first <b>bold</b> paragraph</p>
<p class="text even">second <a href="https://mail.ru">link</a></p>
<p class="list odd">third <a id="paragraph"><b>bold link</b></a></p>
</body>
</html>
"""
from bs4 import BeautifulSoup
soup = BeautifulSoup(html, 'lxml')
print(soup.p, type(soup))
print(soup.p['class'])
print(soup.p.next_sibling.next_sibling)
print(soup.b.parent.name)
print([i.name for i in soup.p.b.parents])
print(soup.p.contents)


html = """<!DOCTYPE html>
<html lang="en">
<head>
<title>test page</title>
</head>
<body class="mybody" id="js-body">
<p class="text odd">first <b>bold</b> paragraph</p>
<p class="text even">second <a href="https://mail.ru">link</a></p>
<p class="text even">second <a href="https://mail.ru">link</a></p>
<p class="list odd">third <a id="paragraph"><b>bold link</b></a></p>
<p class="list odd">third <a id="paragraph"><b>bold link</b></a></p>
</body>
</html>
"""
from bs4 import BeautifulSoup
soup = BeautifulSoup(html, "lxml")
print(soup.p.b.find_parent('body')['class'])
print(soup.p.b.find_parent('body')['id'])
print(soup('p', class_='text odd'))
print(soup('p', class_='list odd'))
print(soup('p', class_='text even'))
print(soup.find(class_='text odd').b.next.next)
print(soup.find_all('p', 'list odd'))
print(soup.select('p.even.text'))
print(soup.select('p.odd.text'))
print(soup.select('a'))
print(soup.select('a > b'))
import re
print(soup.find_all(name=re.compile('^b')))

for i in soup(['a', 'b']):
    print(i)

tag = soup.p

tag.string = 'italic'
print(tag)
print(tag.name)
tag['class'] = 'tag p'
print(tag)

import requests
result = requests.get('http://news.mail.ru/')

soup = BeautifulSoup(result.content, 'lxml')
resp = requests.get('http://www.cbr.ru/ref/blacklist/BlackList.xml')
soup1 = BeautifulSoup(resp.content, "xml")
print(soup1)