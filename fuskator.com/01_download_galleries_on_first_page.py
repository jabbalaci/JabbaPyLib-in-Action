#!/usr/bin/env python

"""
Scrape fuskator.com
===================

Download all galleries on fuskator.com's main page.

Usage:
------
First, specify the base dir in config.py. Galleries will be downloaded
in that directory.

Then just launch this script.

Dependencies:
-------------
This scraper relies on the library jabbapylib.

Tips:
-----
If you don't like a gallery, remove all the images in it and create an empty 
directory called "skip". When you launch the script again, this gallery
will be skipped.
If you don't like some images in a gallery, do the same: remove the images
and create the folder "skip". 
"""

import read_rss
from download_images_from_a_gallery import download_gallery_images

def main():
    items = read_rss.get_items()
    for index,item in enumerate(items):
        print '# gallery {0} of {1}'.format(index+1, len(items))
        download_gallery_images(item.link)
    
    print 'done'
    
#############################################################################

if __name__ == "__main__":
    main()