# info : https://www.crummy.com/software/BeautifulSoup/bs4/doc/

from bs4 import BeautifulSoup
import urllib

url_string = 'https://fivethirtyeight.com/features/political-twitter-is-no-place-for-moderates/'
r = urllib.urlopen(url_string).read()

soup = BeautifulSoup(r)

test = soup.find_all('p')

idx = 0
for entry in test:
    print idx
    print entry.text
    print '\n'
    idx += 1

#print(soup.body.prettify())

#for link in soup.find_all('a'):
#    print(link.get('href'))

#print(soup.get_text())