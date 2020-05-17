from urllib import request, parse
from bs4 import BeautifulSoup
import sys

def WriteFile(url):
    otvet = request.urlopen(url)
    texthtml = otvet.readlines()
    with open('test.html', 'w') as file:
        for line in texthtml:
            file.write(str(line) + "\n")
    with open('test.html', 'r') as file:
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


author = ['Jane Austen', 'Charles Dickens', 'Agatha Christie', 'Thomas Hardy', 'Graham Green', 'William Shakespeare']

header = {}
header['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64 ' \
                       'AppleWebKit/537.36 (KHTML, like Gecko) ' \
                       'Chrome/80.0.3987.132 Safari/537.36'
soup = SearchSomething('query', author[0],"https://www.biography.com/search?", header)


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
print(soup.find('dd', {'itemprop': 'name'}).text)
print('BIRTH DATE:', soup.find('dd', {'itemprop': 'birthDate'}).text)
print('DEATH DATE:', soup.find('dd', {'itemprop': 'deathDate'}).text)

soup = SearchSomething('query', author[0],"http://www.gutenberg.org/ebooks/search/?", header)

allnamebooks = soup.find_all('span', class_='title')
print('LIST OF BOOKS')
namebooks = []
for i in range(len(allnamebooks)):
    if i > 3:
        print(str(allnamebooks[i].text).replace('\\', ''))
        namebooks.append(str(allnamebooks[i].text).replace('\\', ''))
number = 1
linksbooks = soup.find_all('a', class_='link')
url = 'http://www.gutenberg.org' + linksbooks[number + 4].get('href')

soup = WriteFile(url)
links = soup.find_all('a', class_= 'link')
for t in links:
    if 'HTML' in str(t.text):
        url = 'http://www.gutenberg.org' + t.get('href')
        html = request.urlopen(url).read()
        soup = BeautifulSoup(html, 'lxml')

        for element in soup(["script", "style"]):
            element.extract()  # rip it out

        text = soup.get_text()

        with open('test.txt', 'w') as file:
            for line in text:
                file.write(str(line))
        f = open('test.txt')