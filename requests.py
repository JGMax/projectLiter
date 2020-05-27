from urllib import request, parse
from bs4 import BeautifulSoup
import sys
import epub
import os

author = ['Антон Чехов', 'Лев Толстой', 'Иван Тургенев', 'Николай Гоголь', 'Александр Куприн',
          'Николай Лесков', 'Александр Островский', 'Александр Пушкин', 'Михаил Лермонтов', 'Федор Достоевский']
authorenglish = ['Jane Austen', 'Charles Dickens', 'Agatha Christie', 'Thomas Hardy', 'Graham Green', 'William Shakespeare']
def WriteFile(url):
    otvet = request.urlopen(url)
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
    global author
    indexauthor = FindIndex(findname, author)
    soup = SearchSomething('query', author[indexauthor],"https://www.culture.ru/literature/persons?", header)
    linksauthor = soup.find_all('div', class_ = 'entity-card-v2_body')
    nameauthor = soup.find_all('div', class_ = 'card-heading_title')
    i = 0

    for name in nameauthor:
        if str(name.text) == author[indexauthor]:
            url = 'https://www.culture.ru' + linksauthor[i].find('a',{'class':'card-cover'}).get('href')
            break
        i += 1

    soup = WriteFile(url)
    fullbiografy = soup.find('p')
    information = soup.find_all('div', class_ = 'attributes_block')
    biografy = author[indexauthor] + '\n' + 'Годы жизни: ' + information[0].find('div', {'class': 'attributes_value'}).text + '\n'
    biografy += 'Страна рождения: ' + information[1].find('div', {'class': 'attributes_value'}).text + '\n'
    biografy += 'Сфера деятельности: ' + information[2].find('div', {'class': 'attributes_value'}).text + '\n\n'

    count = 1
    for element in fullbiografy.text.split(' '):
        biografy += element
        if count % 11 != 0:
            biografy += ' '
        else:
            biografy += '\n'
            count = 1
        count += 1
    biografy += '\n'
    Transition = soup.find('a', class_ = 'more_btn button button button__neutral button__true')
    url = 'https://www.culture.ru' + Transition.get('href')

    soup = WriteFile(url)

    allnamebooks = soup.find_all('div', class_ = 'card-heading_inner')
    namebooks = []
    for name in allnamebooks:
        if author[indexauthor] == name.find('div', class_ = 'card-heading_subtitle').text and \
                name.find('div', class_ = 'card-heading_list').text != 'Поэзия':
            namebooks.append(name.find('div', class_ = 'card-heading_title').text)
    return (biografy, namebooks, soup,)

def SearchBook(findname, namebooks, soup):

    indexbook = FindIndex(findname, namebooks)
    linksbooks = soup.find_all('div', class_ = 'entity-card-v2_body')
    for name in linksbooks:
        if namebooks[indexbook] == name.find('div', class_ = 'card-heading_title').text:
            url = 'https://www.culture.ru' + name.find('a', {'class': 'card-cover'}).get('href')
    soup = WriteFile(url)
    books = soup.find_all('a', class_ = 'about-entity_btn button button__primary')

    dowlend = books[1].get('href')
    pathfile = os.getcwd()
    pathfile += '\\' + str(namebooks[indexbook]) +'.epub'
    request.urlretrieve(dowlend, pathfile)

    book = epub.open_epub(pathfile)
    with open('book.txt', 'w', encoding = 'utf-8') as file:
        file.write(findname + '\n')
    i = 1
    for item in book.opf.manifest.values():
        data = book.read_item(item)
        if i >= 3 and len(book.opf.manifest.values()) - 2 > i and '?xml' in str(data):
            with open('test.html', 'wb') as file:
                data = data.decode('utf-8').replace('<br/>', ' \n')
                data = data.replace('</p>', ' \n</p>')
                data = data.encode('utf-8')
                file.write(data)
            with open('test.html', 'rb') as file:
                soup = BeautifulSoup(file, 'lxml')
            for element in soup(["script", "style", "title"]):
                element.extract()

            text = soup.get_text().replace("\n\n\n\n\n", "\n")

            with open('book.txt', 'a', encoding = 'utf-8') as file:
                count = 1
                for element in text.split(' '):
                    file.write(element)
                    if '\n' in element:
                        count = 1
                    if count % 11 != 0:
                        file.write(' ')
                    else:
                        file.write('\n')
                        count = 1
                    count += 1
                file.write('\n')
        i += 1
    book.close()
    Delete(pathfile)
    return 'book.txt'

def SearchAboutAuthorEnglish(findname):

    global authorenglish
    indexauthor = FindIndex(findname, authorenglish)
    header = {}
    header['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64 ' \
                       'AppleWebKit/537.36 (KHTML, like Gecko) ' \
                       'Chrome/80.0.3987.132 Safari/537.36'
    soup = SearchSomething('query', authorenglish[indexauthor],"https://www.biography.com/search?", header)


    profession = soup.find_all('div', class_ = 'm-card--label')
    nameauthor = soup.find_all('div', class_ = 'l-grid--item')
    i = 0
    for t in profession:
        a = t.find('a').get('href')
        if str(a) == '/writer':
            url = 'https://www.biography.com' + nameauthor[i].find('phoenix-super-link').get('href')
            break
        i += 1

    soup = WriteFile(url)
    biografy = soup.find('dd', {'itemprop': 'name'}).text + '\n'
    biografy += 'BIRTH DATE: ' + soup.find('dd', {'itemprop': 'birthDate'}).text + '\n'
    biografy += 'DEATH DATE: ' + soup.find('dd', {'itemprop': 'deathDate'}).text + '\n'
    soup = SearchSomething('query', authorenglish[indexauthor],"http://www.gutenberg.org/ebooks/search/?", header)

    allnamebooks = soup.find_all('span', class_='title')

    namebooks = []
    for i in range(len(allnamebooks)):
        if i > 3:
            namebooks.append(str(allnamebooks[i].text).replace('\\', ''))
    return (biografy, namebooks, soup,)

def SearchBookEnglish(findname, namebooks, soup):

    linksbooks = soup.find_all('a', class_='link')
    indexbook = FindIndex(findname, namebooks)
    url = 'http://www.gutenberg.org' + linksbooks[indexbook + 4].get('href')
    soup = WriteFile(url)
    links = soup.find_all('a', class_= 'link')
    for link in links:
        if 'More' in str(link.text):
            url = 'http://www.gutenberg.org' + link.get('href')
            soup = WriteFile(url)
            links = soup.find_all('a')
            for text in links:
                if '.txt' in str(text.text):
                    dowlend = url + text.get('href')
                    pathfile = os.getcwd()
                    pathfile += '\\' + 'bookenglish.txt'
                    request.urlretrieve(dowlend, pathfile)

    return 'bookenglish.txt'