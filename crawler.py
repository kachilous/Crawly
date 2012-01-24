#Web Crawler

import urllib2
import re
from BeautifulSoup import BeautifulSoup
from collections import deque

depth = 0
i = 0
j = -10

#this function will check to see if a link is valid
def validate(n):
	try:
		currenturl = urllib2.urlopen(n) 
		return 1
	except urllib2.URLError:
		return 0
		
def visited_test(n):
	for x in visited:
		if n == x:
			break
			return 0
	return 1
	
def unvisited_test(n):
	for y in unvisited:
		if n == y:
			break
			return 0
	return 1

url_seed = raw_input("Please enter a url seed: ");
string = raw_input("Please enter search string: ");
max_depth = int(raw_input("Please enter the max depth to crawl to: "));
	
#create visited and unvisited lists as well as a temp list to hold unvisited links during iteration
unvisited = []
visited = []
temp = []

#append the url seed to the unvisited list
unvisited.append(url_seed)

currenturl = unvisited.pop(0)

while(depth < max_depth):	
	try:
		#open the url for parsing
		url = urllib2.urlopen(currenturl) 
		
		#create BeautifulSoup object
		soup = BeautifulSoup(url) 
		
		#this will see if string is on current html page
		#regexp is looking for an occurrence of string not the exact match to the NavigableString string
		find_string = soup.body.findAll(text=re.compile(string), limit=1) 
		
		#if the keyword is found, print that the string is not on the currenturl
		if find_string == []: 
			print string, "was not found on the page: ", currenturl 
		#otherwise, print that the keyword was not foudn on the currenturl
		else: 
			print string, "was found on the page: ", currenturl
		
		#Find all links in anchor tags and extract only the links
		if soup != None:
			links =  soup.findAll('a', href = re.compile("http://")) 
			
		#this should only happen once, since unvisited list won't be populated with links in the first iteration
		if(unvisited == [] and visited == []):
			for link in links:
				if validate(link['href']) == 1 and visited_test(link['href']) == 1 and unvisited_test(link['href']) == 1 and len(temp) < 10:
					temp.append(link['href'])
					
		#Loop through all links and check to see if link is valid and not in visited or unvisited list -> if so then add link to a temporary list [threshold is 50]
		else:
			for link in links:
				if validate(link['href']) == 1 and visited_test(link['href']) == 1 and unvisited_test(link['href']) == 1 and len(temp) < 10:
					temp.append(link['href'])
					
									
		#Add recently fetched links to the beginning of unvisited
		unvisited.extend(temp)
		
		#free memory in temp list
		del temp[:]
			
		#each time temp list is filled with 10 new links, a new depth has been reached
		depth = depth + 1

		#move current url to visited list
		visited.append(currenturl)
		
		#Pop the next j += 10 link from the unvisited list
		j = j + 10
		currenturl = unvisited.pop(j)

	except ValueError, urllib2.URLError:
		if unvisited != []:
			currenturl = unvisited.pop()
		else:
			print "Oops!", currenturl, "is not a valid url and there are no more links to parse"
			break