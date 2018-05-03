__author__ = 'Brendan'

from bs4 import BeautifulSoup
import requests
import json
#import urllib


#################################3
# control panel

url_string = 'https://www.socialseer.com/resources/us-senator-twitter-accounts/'
target_filename = 'senator twitter usernames.json'
user_agent = 'Chrome/6.0.472.63 Safari/534.3'

#################################


###
'''
class AppURLopener(urllib.request.FancyURLopener):
    #version = "Mozilla/5.0"
    version = "Chrome/6.0.472.63 Safari/534.3"
'''
###



def build_list(url_string):

    '''
    opener = AppURLopener() # create a user agent to perform with the web request
    response = opener.open(url_string)
    print response
    r = response.read()
    print r
    '''

    senator_usernames = []
    senator_URLs = []

    response = requests.get(url_string,headers={"User-agent":user_agent})
    # warning should check for [Response [200]> here
    print response
    r = response.text

    # use beautiful soup to grab the table entry data
    soup = BeautifulSoup(r)
    full_table = soup.find_all('a',href=True)

    #for link in BeautifulSoup(r, parseOnlyThese=SoupStrainer('a')):
    #    if link.has_attr('href'):
    #        print link['href']

    idx = 0
    for entry in full_table:
        putative_handle = entry.text
        putative_url = entry['href']

        # check if text looks like a twitter handle
        if hasattr(entry,'text'):
            if len(entry.text) > 0:
                if entry.text[0] == '@':
                    # add this to list of users
                    senator_usernames.append(putative_handle)
                    senator_URLs.append(putative_url)

            idx += 1

    print([str(idx), " total users"])

    print senator_usernames
    print senator_URLs

    # write the lists to json files
    target_file = open(target_filename,'w')
    json.dump({"senator_usernames":senator_usernames,"senator_URLs":senator_URLs},target_file,indent=2)







#print(soup.body.prettify())

#for link in soup.find_all('a'):
#    print(link.get('href'))

#print(soup.get_text())


build_list(url_string)


