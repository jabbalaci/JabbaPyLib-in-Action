#!/usr/bin/env python

from jabbapylib.web.web import get_page #@UnresolvedImport
from jabbapylib.web.scraper import bs #@UnresolvedImport
from jabbapylib.console import color #@UnresolvedImport

# pretty print numbers
import locale
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

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
        print '{blog:40}{hits:>10n}'.format(blog=key, hits=dic[key])
        summa += dic[key]
    #
    print '-' * (40+10)
    print '{total} number of visits: {hits}!'.format(
        total=color.bold('Total'),                                          
        hits=color.bold('{0:n}'.format(summa))
    )


def main():
    dic = {}
    for b in blogs:
        visit(b, dic)
        
    print_result(dic)

#############################################################################

if __name__ == '__main__':
    main()
