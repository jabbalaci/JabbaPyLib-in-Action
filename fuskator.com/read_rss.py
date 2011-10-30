#!/usr/bin/env python

"""
It's a module but also a standalone script.

Downloads fuskator.com's RSS and extracts the items.
One item is one gallery.
"""

import untangle
import common

XML = 'http://fuskator.com/rss/home.rss'

class Item:
    def __init__(self, item):
        self.title = item.title.cdata
        self.description = item.description.cdata
        self.link = item.link.cdata
        self.guid = item.guid.cdata
        self.pub_date = common.simplify_date(item.pubDate.cdata)
        
    def __str__(self):
        sb = []
        for key in self.__dict__:
            sb.append("{key}='{value}'".format(key=key, value=self.__dict__[key]))
             
        return ', '.join(sb)
    
    def __repr__(self):
        return self.__str__()
    

def get_items():
    items = []
    
    o = untangle.parse(XML)
    
    for item in o.rss.channel.item:
        items.append(Item(item))

    return items

#############################################################################

if __name__ == "__main__":
    li = get_items()
    print "# number of items:", len(li)
    for it in li:
        print it.link
    print li[0]