#!/usr/bin/env python

"""
This script is a module but it can also be used as a 
standalone script.

If you specify a gallery URL, this script will download
that gallery.

While 01_download_galleries_on_first_page.py only downloads
galleries _on the main page_, with this script you can
download any gallery on fuskator.com.
"""

import re
import sys

from random import shuffle

from get_image_urls_in_gallery import extract_image_urls
from jabbapylib.web import web
from jabbapylib.web.download.image import Image
from common import get_subdir_name
from jabbapylib.autoflush.autoflush import unbuffered
import jabbapylib.web.scraper.scraper as scraper
import config as cfg

FUSKATOR = 'fuskator.com'

def download(url, origin, image_urls):
    print '# debug:', url
    li = []
    for img_url in image_urls:
        img_obj = Image(cfg.BASE_DIR, get_subdir_name(url), img_url)
        readme = """origin:   {origin}
fuskator: {fuskator}
{urls}
""".format(origin=origin, fuskator=url, urls='\n'.join([x for x in image_urls]))
        img_obj.readme = readme
        li.append(img_obj)
        
    unbuffered()
    
    shuffle(li)     # randomize the order, 
                    # think of the webserver log too ;)
        
    if len(li) > 0:
        print '#', url
        print '# number of images:', len(li)
        print '# download dir.:', li[0].get_local_dir()
        for img in li:
            img.download()
            sys.stdout.write('.')
            if cfg.SLEEP_BETWEEN_IMAGES:
                scraper.sleep(3,3)
        print
    

def download_gallery_images(url):
    if web.get_host(url) != FUSKATOR:
        print >>sys.stderr, "# warning: the site {site} is not supported.".format(site=web.get_host(url))
        return
    # else, if it's the FUSKATOR site
    url = url.replace('/full/', '/thumbs/')
    origin, image_urls = extract_image_urls(url)
    download(url, origin, image_urls)
    
#############################################################################

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print "Error: you must specify a gallery URL."
        sys.exit()
    # else
    #url = 'http://fuskator.com/thumbs/lnf8cHriPBu/Caprice_hegre_solo_Super+Model_teen_tfpez_trimmed.html'
    download_gallery_images(sys.argv[1])
    