#!/usr/bin/env python

"""
This is a module but it can also be used as a standalone script.

Specify a gallery and it extracts the image URLs.

The gallery must be in thumbs format, i.e. the URL must look like
this: http://fuskator.com/thumbs/...
"""

import re

from jabbapylib.web.scraper import bs
from jabbapylib.web.web import get_page

def extract_image_urls(url):
    origin = None
    li = []
    
    text = get_page(url, user_agent=True, referer=True)
    soup = bs.to_soup(text)
    
#    this version worked for a day:
#    for pic in soup.findCssSelect('div.pic'):
#        a = pic.find('a', href=True)
#        if a:
#            li.append(a['href'])

#   here is a new version, updated to the changes
    for div in soup.findCssSelect('div.pic'):
        img = div.find('img')
        if img and img.has_key('src'):
            li.append(img['src'].replace('/small/', '/large/'))
        
    for div in soup.findCssSelect('html body form#aspnetForm div#main div'):
        result = re.search(r'URL: (http://.*)View full images', div.text)
        if result:
            origin = result.group(1)
            
    return origin, li

#############################################################################

if __name__ == "__main__":
    url = 'http://fuskator.com/thumbs/lnf8cHriPBu/Caprice_hegre_solo_Super+Model_teen_tfpez_trimmed.html'
    origin, image_urls = extract_image_urls(url)
    print '#', origin
    for img in image_urls:
        print img
