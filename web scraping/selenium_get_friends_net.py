__author__ = 'Brendan'

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import json
import numpy as np

import os
import sys
import codecs
import pprint


from selenium import webdriver
import selenium.webdriver.support.ui as ui



####################
twitter_login_url = "https://twitter.com/login"

SECRET_EMAIL = "obfuscated"
SECRET_PASSWORD = 'obfuscated"

reference_user = 'texastacos' # center of the desired neighborhood
#reference_user = 'societyoftrees'
target_filename = 'texas_tacos_friend_neighborhood.json'
#target_filename = 'societyoftrees_friend_neighborhood.json'


####################
# these should be refactored into a 'user' class and held in a db or something


#followers_list_urls = [] # handle (full link to user home) # todo
#followers_list_titles = [] # short name

celeb_cutoff = 1000

####################

def init_driver():
    driver = webdriver.Firefox()
    driver.wait = WebDriverWait(driver, 10) # probably only need one of these wait parameters?
    driver.implicitly_wait(10)
    return driver


def visit_user(driver, username):

    #time.sleep(1)
    user_home_url = "https://www.twitter.com/"  + username
    driver.get(user_home_url)
    #time.sleep(1)

    # reminder - try to switch to frame defined by page-container

    #stats_xpath = "//div[@id='page-container']/div/div/div/div/ul/li/a/span[@class='ProfileCardStats']"
    stats_xpath = "//div[contains(@id,'page-container')]"  # /li/a"

    #stats_xpath = r"//*[@id='page-container']/div[1]/div[1]/div/div[3]/ul/li[1]/a/span[2]" # testing
    stats_spans = driver.find_elements_by_xpath(stats_xpath)

    #time.sleep(1)
    #print followers_span.value

    #print " here is the list returned by web driver:"
    #print stats_spans
    #print " grab html of the page container :"
    #print stats_spans[0].get_attribute('outerHTML') # num tweets

    soup = BeautifulSoup(stats_spans[0].get_attribute('outerHTML')) # todo shouldn't need to import beautiful soup for this, selenium has this capability
    profile_stats_panel = soup.find_all('span','ProfileNav-value')
    num_tweets = process_html_numeral(profile_stats_panel[0])
    num_friends = process_html_numeral(profile_stats_panel[1])
    num_followers = process_html_numeral(profile_stats_panel[2])

    print "user " + username  + " has [tweets, friends, followers] = " + str(num_tweets) + "," + str(num_friends) + "," + str(num_followers)
    return num_tweets, num_friends, num_followers

def process_html_numeral(item):
    raw_text = item.text
    print raw_text
    text = raw_text.replace(',','')
    text = text.replace('.','')
    text = text.replace('K','000')
    text = text.replace('M','000000')
    numeral = int(text)
    return numeral

def grab_friends(driver, username, total_friends): # generate friends list
    friend_list_urls = [] # handle (full link to user home)
    friend_list_titles = [] # short name
    friend_list_usernames = []

    target_url = "https://twitter.com/" + username + "/following"
    if driver.current_url != target_url:
        driver.get(target_url)

    users_xpath = "//div[@class='ProfileCard-content']/a"

    friend_detection_counter = 0
    counter_prior_step = friend_detection_counter
    counter_prior_step_intermediate = friend_detection_counter

    while friend_detection_counter < total_friends: # inf loop here

        users_on_page = driver.find_elements_by_xpath(users_xpath) # refresh the user list
        print str(len(users_on_page)) + " users detected on page"
        print "friend_detection_counter = " + str(friend_detection_counter)
        print "total_friends = " + str(total_friends)

        for user in users_on_page[friend_detection_counter:]: # take the sublist beginning with the last detected entry

            user_link = user.get_attribute('href')   # grab the usernames on the page
            user_title = user.get_attribute('title')
            this_username = user_link.replace("https://twitter.com/","")
            #user_link = users_on_page[friend_detection_counter].get_attribute('href')
            #user_title = users_on_page[friend_detection_counter].get_attribute('title')
            friend_list_urls.append(user_link)
            friend_list_titles.append(user_title)
            friend_list_usernames.append(this_username)
            #print user_link
            friend_detection_counter += 1  # update the counter

        # scroll down to load more entries
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        ##################### check for page loading problems...
            #  if no friends found on this step - something went wrong
        if counter_prior_step == friend_detection_counter:
            # then try again
            print "something went wrong...restarting scan of friends for this user"
            driver.get(target_url) # refresh the page
            [friend_list_urls, friend_list_titles, friend_list_usernames] = grab_friends(driver, username, total_friends)
            break # exit the outer while loop

        if counter_prior_step_intermediate == friend_detection_counter:
            # problem scrolling - wait a second before trying one more time
            time.sleep(3)


        counter_prior_step = counter_prior_step_intermediate # keep track of two steps back
        counter_prior_step_intermediate = friend_detection_counter # update

    # return friend list
    return friend_list_urls, friend_list_titles, friend_list_usernames


def twitter_login(driver, twitter_login_url):
    driver.get(twitter_login_url)

    user_xpath = "//input[@name='session[username_or_email]']"
    username_field = driver.find_elements_by_xpath(user_xpath)[1] # there are several elements with this xpath ... only the 2nd of 3 is interactable
    #time.sleep(3)
    #username_field.click()
    username_field.send_keys(SECRET_EMAIL)

    pwd_xpath = "//input[@name='session[password]']"
    pwd_field = driver.find_elements_by_xpath(pwd_xpath)[1] # there are several elements with this xpath ... only the 2nd of 3 is interactable
    pwd_field.send_keys(SECRET_PASSWORD)

    button_xpath = "//*[@id='page-container']/div/div[1]/form/div[2]/button"
    button = driver.find_element_by_xpath(button_xpath)
    button.click() # submit form

    wait = ui.WebDriverWait(driver, 1)
    #alert = driver.switch_to_alert() # switch to popup window

def crawl_friend_neighborhood(driver, reference_user, friend_list_usernames):

    celeb_list = []

    neighborhood = [reference_user] # populate the node set
    #
    for friend in friend_list_usernames:
        neighborhood.append(friend)

    W_friends = np.zeros((len(neighborhood),len(neighborhood)))
    W_friends[0,:] = 1 # we already know this connectivity

    for friend_idx,neighbor in enumerate(friend_list_usernames):
        # get followers_list
        neighborhood_idx = friend_idx + 1 # b/c first entry is reference user
        [num_tweets, num_friends, num_followers] = visit_user(driver, neighbor)
        if num_friends <= celeb_cutoff:
            # get friend list
            print "geting friends list for user " + neighbor + "..."
            friends_of_friend = grab_friends(driver,neighbor,num_friends)
            for potential_friend in friends_of_friend:
                if potential_friend in neighborhood:
                    neighborhood_post_idx = neighborhood.index(potential_friend)
                    W_friends[neighborhood_idx,neighborhood_post_idx]
            # check for
        else:
            print "warning, " + neighbor + " is a celebrity...not processing friends"
            W_friends[neighborhood_idx,:] = -1 # mark these links as invalid
            celeb_list.append(neighbor)

    return W_friends, celeb_list, neighborhood  # temp

if __name__ == "__main__":
    driver = init_driver()
    twitter_login(driver, twitter_login_url)

    print "reference user: " + reference_user

    [num_tweets, num_friends, num_followers] = visit_user(driver, reference_user)
    if num_friends > celeb_cutoff:
        print "WARNING reference user is a celebrity with a large number of friends...this script is not meant for this."

    [friend_list_urls, friend_list_titles, friend_list_usernames] = grab_friends(driver, reference_user, num_friends)

    [W_friends,celeb_list,neighborhood] = crawl_friend_neighborhood (driver, reference_user, friend_list_usernames) # populate

    driver.quit()

    # write the friend list to a json file
    save_object = {"neighborhood":neighborhood,"W_friends":W_friends.tolist(),"celeb_list":celeb_list,
                   "friend_urls":friend_list_urls, "friend_titles":friend_list_titles} # don't really need these lower line lists right?}
    target_file = open(target_filename,'w')
    json.dump(save_object,target_file, indent=2)
