#Web Crawler

import urllib2
import re
from BeautifulSoup import BeautifulSoup
from httplib import BadStatusLine

depth = 0

#this function will see if a link is valid
def validate(n):
    try:
        currenturl = urllib2.urlopen(n) 
	return 1
    except (urllib2.URLError, BadStatusLine, urllib2.HTTPError):
	return 0
		
#this function will see if a link is already in the visited list
def visited_test(n):
    if visited.count(n) == 0:
	return 1
    return 0
	
#this function will see if a link is already in the unvisited list
def unvisited_test(n):
    if unvisited.count(n) == 0:
        return 1
    return 0
	
#user has to enter a valid url
while 1:
    try:
        url_seed = raw_input("Please enter a url seed: ");
	test = urllib2.urlopen(url_seed)
	break
    except (urllib2.URLError, BadStatusLine, urllib2.HTTPError):
        print "Oops! Please enter a valid link"

string = raw_input("Please enter search string: ");

#user has to enter an integer 
while 1:
    try:
        max_depth = int(raw_input("Please enter the max depth to crawl to: "));
        break
    except (ValueError):
        print "Ooops! Please enter an integer"

print "\n"
	
#create visited and unvisited lists as well as a temp list to hold unvisited links during iteration
unvisited = []
visited = []
temp = []

#append the url seed to the unvisited list
unvisited.append(url_seed)

currenturl = unvisited.pop(0)

#keep looping until user's max_depth is reached or there are no more links to parse
while(depth < max_depth):	
    try:
        #move current url to visited list
	visited.append(currenturl)
			
	#open the url for parsing
	url = urllib2.urlopen(currenturl) 
		
	#create BeautifulSoup object
	soup = BeautifulSoup(url)
		
        if soup != None:
            #this will see if the keyword is on the current html page
            #regexp looks for an occurence of the keyword
            find_string = soup.findAll(text=re.compile(string), limit=1)
        else:
            print "could not search", currenturl, "for", string
		
	#if the keyword is not found, print that the keyword was not found on the currenturl
	if find_string == []: 
            print string, "was not found on the page: ", currenturl 
	#otherwise, print that the keyword was found on the currenturl
	else: 
            print string, "was found on the page: ", currenturl

        #reset list
        find_string = []
		
	#Find all html links in anchor tags and extract only the url
	if soup != None:
            links =  soup.findAll('a', href = re.compile("http://")) 
			
	#this should only happen once, since unvisited list won't be populated with links in the first iteration
	if(unvisited == [] and visited == []):
            for link in links:
                if validate(link['href']) == 1 and visited_test(link['href']) == 1 and unvisited_test(link['href']) == 1 and len(temp) < 10:
                    if temp.count(link['href']) == 0:
                        temp.append(link['href'])
					
	#Loop through all links and check to see if link is valid and not in visited or unvisited list -> if so then add link to a temporary list [max is 10]
	else:
            for link in links:
                if validate(link['href']) == 1 and visited_test(link['href']) == 1 and unvisited_test(link['href']) == 1 and len(temp) < 10:
                    if temp.count(link['href']) == 0:
                        temp.append(link['href'])
									
	#Add recently fetched links to the end of unvisited list
	unvisited.extend(temp)
		
	#if no links were received during current iteration, fetch link from previous iteration; if there are no links in unvisited list break out of loop
	if len(temp) == 0:
            if len(unvisited) != 0:
                firstlink = unvisited.pop()
                print "no valid links were found on", currenturl, "retrieving new link..."
                currenturl = firstlink
	    else:
                print "there are no more links in the unvisited list"
                break

	#otherwise, fetch first link retrieved during current iteration
	else:
            firstlink = temp.pop(0)

            #pop link from unvisited
            unvisited.remove(firstlink)
		
	    #free memory in temp list
	    del temp[:]
			
	    #each time temp list is filled with n new links, a new depth has been reached
	    depth = depth + 1
	    print "current depth is", depth
	    print "\n"

	    #set current url to link just fetched
	    currenturl = firstlink
		
    except (ValueError, urllib2.URLError, BadStatusLine, urllib2.HTTPError):
        #if error occurs while trying to open link, throw exception and pop a new link if there is one
        if unvisited != []:
	    currenturl = unvisited.pop()
	#otherwise, alert the user that their link is invalid and there are no more links
	else:
	    print "Unfortunately there are no more links to parse"
	    break
