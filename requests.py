from urllib import request, parse
from bs4 import BeautifulSoup
import sys
import epub

def WriteFile(url):
    otvet = request.urlopen(url)
    #otvet.encoding = 'utf-8'
    texthtml = otvet.readlines()
    with open('test.html', 'wb') as file:
        for line in texthtml:
            file.write(line)
    with open('test.html', 'rb') as file:
        soup = BeautifulSoup(file, 'lxml')
    return soup
def SearchSomething(key, value, website, header):
    query = { key : value}
    try:
        data = parse.urlencode(query)
        website += data
        req = request.Request(website, headers = header)
        return WriteFile(req)
    except Exception:
        print('Error occuried during web request!!')
        print(sys.exc_info()[1])


author = ['Антон Чехов', 'Лев Толстой', 'Иван Тургенев', 'Николай Гоголь', 'Александр Куприн',
          'Михаил Булгаков', 'Максим Горький', 'Виктор Астафьев', 'Александр Солженицын', 'Федор Достоевский']

header = {}
header['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64 ' \
                       'AppleWebKit/537.36 (KHTML, like Gecko) ' \
                       'Chrome/80.0.3987.132 Safari/537.36'
indexauthor = 1
indexbook = 0
soup = SearchSomething('query', author[indexauthor],"https://www.culture.ru/literature/persons/writer?", header)

linksauthor = soup.find_all('div', class_ = 'entity-card-v2_body')
nameauthor = soup.find_all('div', class_ = 'card-heading_title')
i = 0

for name in nameauthor:
    if str(name.text) == author[indexauthor]:
       url = 'https://www.culture.ru' + linksauthor[i].find('a',{'class':'card-cover'}).get('href')
       break
    i += 1

soup = WriteFile(url)


byografy = soup.find_all('div', class_ = 'attributes_block')
with open('byografy.txt', 'w') as file:
    file.write('Годы жизни: ' + byografy[0].find('div', {'class': 'attributes_value'}).text + '\n')
    file.write('Страна рождения: ' + byografy[1].find('div', {'class': 'attributes_value'}).text + '\n')
    file.write('Сфера деятельности: ' + byografy[2].find('div', {'class': 'attributes_value'}).text + '\n')


Transition = soup.find('a', class_ = 'more_btn button button button__neutral button__true')
url = 'https://www.culture.ru' + Transition.get('href')
soup = WriteFile(url)
#soup = SearchSomething('query', author[0],"https://www.culture.ru/literature/books/author?", header)
allnamebooks = soup.find_all('div', class_ = 'card-heading_head')

namebooks = []
for name in allnamebooks:
    if author[indexauthor] == name.find('div', class_ = 'card-heading_subtitle').text:
        namebooks.append(name.find('div', class_ = 'card-heading_title').text)

linksbooks = soup.find_all('div', class_ = 'entity-card-v2_body')
for name in linksbooks:
    if namebooks[indexbook] == name.find('div', class_ = 'card-heading_title').text:
        url = 'https://www.culture.ru' + name.find('a', {'class': 'card-cover'}).get('href')


soup = WriteFile(url)

books = soup.find_all('a', class_ = 'about-entity_btn button button__primary')
dowlend = books[1].get('href')
myFile = 'D:\\myprogramms\\literature\\'+ str(namebooks[indexbook]) +'.epub'
request.urlretrieve(dowlend, myFile)


book = epub.open_epub(myFile)
with open('book.txt', 'w', encoding = 'utf-8') as file:
    pass
i = 1
for item in book.opf.manifest.values():
    data = book.read_item(item)
    if i >= 3 and len(book.opf.manifest.values()) - 1 > i:
        with open('test.html', 'wb') as file:
            file.write(data)
        with open('test.html', 'rb') as file:
            soup = BeautifulSoup(file, 'lxml')
        books = soup.find_all('p')
        with open('book.txt', 'a', encoding='utf-8') as file:
            for line in books:
                count = 0
                for element in line.text.split(" "):
                    count += 1
                    file.write(element)
                    if count % 15 != 0:
                        file.write(' ')
                    else:
                        file.write('\n')
                        count = 0
                file.write('\n')

    i += 1