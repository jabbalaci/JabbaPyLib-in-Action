#!/usr/bin/env python

from jabbapylib.web.web import get_page
from jabbapylib.web.scraper import bs
from jabbapylib.number.number import number_to_pretty_string
from jabbapylib.console import color

blogs = ['pythonadventures', 'ubuntuincident']


def visit(blog, dic):
    url = 'http://{name}.wordpress.com'.format(name=blog)
    text = get_page(url)
    soup = bs.to_soup(text)
    hits = soup.findCssSelect('div#blog-stats ul li')[0].text
    hits = int(hits.replace('hits','').replace(',','').strip())
    #
    dic[url] = hits


def print_result(dic):
    summa = 0
    for key in sorted(dic.keys()):
        print '{blog:40}{hits:>10}'.format(blog=key, hits=number_to_pretty_string(dic[key]))
        summa += dic[key]
    #
    print '-' * (40+10)
    print '{total} number of visits: {hits}!'.format(
        total=color.bold('Total'),                                          
        hits=color.bold(number_to_pretty_string(summa))
    )


def main():
    dic = {}
    for b in blogs:
        visit(b, dic)
        
    print_result(dic)

#############################################################################

if __name__ == '__main__':
    main()
