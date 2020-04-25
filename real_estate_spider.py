from robotsreader import robots_txt_reader  # help(robots_txt_reader)
import urllib.request
from bs4 import BeautifulSoup
import csv
import time
import html5lib

# defining url for pass-through
# # # # # url_input = input('input url to scrub: ')
url_input = 'http://www.topleaguecityhomes.com'
url = (url_input + '/robots.txt')

print(url)
# unpacking results from robots_txt_reader
results = robots_txt_reader(url)
sitemaps = results[0]     # set by robots.txt
disallow = results[1]     # set by robots.txt
crawl_delay = results[2]  # set by robots.txt
message = results[3]      # set by robots.txt
print(message)

time.sleep(crawl_delay)  # following crawl delay set by website. we only make kind spiders

##################### Left off here, I am only getting the first 8 responses for some reason. possibly due to urllib2 which is urllib,request

request = urllib.request.Request(url_input)  # send request to site
html = urllib.request.urlopen(request).read()  # open URL and download HTML content
print(html)
soup = BeautifulSoup(html, 'html5lib')  # pass the HTML to BeautifulSoup
# get HTML of table called site Table where all the links are displayed
main_table = soup.find("div", class_="row property-photo-grid")                 # only works for topleaguecityhomes.com
# Go into main_table and get every a element in it which has class 'title'
links = main_table.find_all("a") # only works for topleaguecityhomes.com
print(len(links), len(main_table))
# from each link extract the text of link and the link itself
# List to store href values on page
extracted_records = []
for link in links:
    extracted_records.append(link.get('href'))

for record in extracted_records:
    new_url = url_input + record
    print(new_url)

