from urllib import request, parse
from bs4 import BeautifulSoup
import sys
import epub
import os

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

def FindIndex(name, search):
    for i in range(len(search)):
        if name == search[i]:
            return i

def Delete(myFile):
    os.remove(myFile)
def SearchAboutAuthor(findname):

    header = {}
    header['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64 ' \
                           'AppleWebKit/537.36 (KHTML, like Gecko) ' \
                           'Chrome/80.0.3987.132 Safari/537.36'
    author = ['Антон Чехов', 'Лев Толстой', 'Иван Тургенев', 'Николай Гоголь', 'Александр Куприн',
          'Михаил Булгаков', 'Максим Горький', 'Виктор Астафьев', 'Александр Солженицын', 'Федор Достоевский']

    indexauthor = FindIndex(findname, author)
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


    information = soup.find_all('div', class_ = 'attributes_block')
    biografy = author[indexauthor] + '\n' + 'Годы жизни: ' + information[0].find('div', {'class': 'attributes_value'}).text + '\n'
    biografy += 'Страна рождения: ' + information[1].find('div', {'class': 'attributes_value'}).text + '\n'
    biografy += 'Сфера деятельности: ' + information[2].find('div', {'class': 'attributes_value'}).text + '\n'

    Transition = soup.find('a', class_ = 'more_btn button button button__neutral button__true')
    url = 'https://www.culture.ru' + Transition.get('href')

    soup = WriteFile(url)

    allnamebooks = soup.find_all('div', class_ = 'card-heading_head')
    namebooks = []
    for name in allnamebooks:
        if author[indexauthor] == name.find('div', class_ = 'card-heading_subtitle').text:
            namebooks.append(name.find('div', class_ = 'card-heading_title').text)
    return (biografy, namebooks, soup, )

def SearchBook(findname, namebooks, soup):

    indexbook = FindIndex(findname, namebooks)
    linksbooks = soup.find_all('div', class_ = 'entity-card-v2_body')
    for name in linksbooks:
        if namebooks[indexbook] == name.find('div', class_ = 'card-heading_title').text:
            url = 'https://www.culture.ru' + name.find('a', {'class': 'card-cover'}).get('href')
    soup = WriteFile(url)
    books = soup.find_all('a', class_ = 'about-entity_btn button button__primary')
#soup = WriteFile(url)
    dowlend = books[1].get('href')
    pathfile = os.getcwd()
    pathfile += '\\' + str(namebooks[indexbook]) +'.epub'
    request.urlretrieve(dowlend, pathfile)

    book = epub.open_epub(pathfile)
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
            with open('book.txt', 'a', encoding = 'utf-8') as file:
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
    book.close()
    Delete(pathfile)
    return 'book.txt'