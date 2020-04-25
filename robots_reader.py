def robots_txt_reader(url):
    """ Takes url and returns:
    results(sitemaps, disallow, crawl_delay, message) -- for python spider. """

    import urllib.request
    from bs4 import BeautifulSoup

    request = urllib.request.Request(url)
    html = urllib.request.urlopen(request).read()
    sorted_list = []
    holder_list = []

    # pass the HTML to BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')
    soupstr = soup.get_text() # changes BS4 type to str type

    soup_sort = soupstr.split('\n')  # split text string into list based on '\n'

    # remove anything in robots.txt with "#"
    for item in soup_sort:
        if not item.find("#"):
            soup_sort.remove(item)

    # Check if soup_sort starts with ''
    if soup_sort[0] == '':
        del soup_sort[0]  # remove '' from start of soup_sort

    # Check if soup_sort ends in ''
    if soup_sort[-1] != '':
        soup_sort.append("")  # add '' to end of soup_sort

    # splits list into sub-lists based on ''
    for item in soup_sort:
            if item == '':
                sorted_list.append(holder_list)
                holder_list = []

            else:
                holder_list.append(item)

    # robots.txt is now broken into subsets in sorted_list

    # Goes through sorted list and categorizes
    agent_and_rule = []  # store location
    sitemap = []  # store location
    for item in sorted_list:
        for subitem in item:
            if not subitem.find("User-agent"):  # if subitem has User-agent, move to agent_and_rule
                agent_and_rule.append(item)
            elif not subitem.find("Sitemap: "):  # if subitem has Sitemap, move to sitemap
                sitemap.append(subitem)


    spider_must_follow = []
    for item in agent_and_rule:
        for subitem in item:
            if not subitem.find('User-agent: *'): # if subitem has 'User-agent: *', move to spider_must_follow
                spider_must_follow.append(item)

    rules = []
    for item in spider_must_follow:
        for subitem in item:
            if subitem.find('User-agent: *'): # every subitem that isn't 'User-agent: *' is added to rules
                rules.append(subitem)


    # now all rules applicable to 'User-agent: *' (this spider) are stored in rules


    # creates crawl_delay to pass through
    for item in rules:
            if not item.find('Crawl-delay: '): # if there is a crawl delay, set that to a variable
                crawl_delay = item.split(": ", 1)
                crawl_delay = int(crawl_delay[1])

    # creates message to pass through
    for item in rules:
            if item == 'Disallow: /':
                message = 'All robots excluded from this server'
            elif item == 'Disallow: ':
                message = 'All robots allowed and full access'
            else:
                message = ''

    # creates sitemaps to pass through
    sitemaps = []
    for item in sitemap:
            if not item.find('Sitemap: '): # if there is a sitemap, add to sitemaps list
                sites = item.split("Sitemap: ")
                site = sites[1::2]
                sitemaps += site
            else:
                sitemaps = []

    # creates disabled to pass through
    disallow = []
    for item in rules:
            if not item.find('Disallow: '): # if there is a disallow, add to disallowed list
                dis = item.split("Disallow: ")
                disal = dis[1::2]
                disallow += disal
            else:
                disallow = []
    results = (sitemaps, disallow, crawl_delay, message)
    return results
# pass-through : (sitemaps(list), disallow(list), crawl_delay, message)
# can probably cut this program here and pass through to spider

