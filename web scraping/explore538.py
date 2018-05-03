# info : https://www.crummy.com/software/BeautifulSoup/bs4/doc/

from bs4 import BeautifulSoup
import urllib

url_string = 'http://www.reddit.com'
r = urllib.urlopen(url_string).read()

soup = BeautifulSoup(r)


test = soup.find_all('div')
idx = 0
for entry in test:
    print idx
    print entry.prettify()
    print '\n'
    print '\n'
    print '\n'

    idx += 1



#print(soup.body.prettify())

#for link in soup.find_all('a'):
#    print(link.get('href'))

#print(soup.get_text())