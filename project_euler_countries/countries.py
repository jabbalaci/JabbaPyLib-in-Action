#!/usr/bin/env python

"""
Analyze the statistics page of Project Euler (http://projecteuler.net/index.php?section=statistics)
and make a new stat. page where the countries are sorted by strength.

A country is considered to be strong if it has lots of participants.

Usage:
======
First visit the stat. page with Firefox. Since you will have to log in to the PE
site for that, the necessary cookies will be stored in Firefox's cookies.sqlite file.
This script will have to use those cookies in order to fetch the stat. page. The
output will be written to 'stat.html' by default.

TODO: the current version shows the absolute strength of the countries. Add
an option to calculate the relative strength too, where the population of
a given country is taken into account. The population could be gathered from
Wikipedia for instance and stored in a file.
"""

URL = 'http://projecteuler.net/index.php?section=statistics'
LOGIN = 'http://projecteuler.net/index.php?section=login'
HEADER1 = 'assets/header_1.html'
HEADER2 = 'assets/header_2.html'
FOOTER = 'assets/footer.html'
OUTPUT = 'stat.html'

import re
import sys
import operator
import webbrowser

import jabbapylib.web.web as web
from BeautifulSoup import BeautifulSoup


class Countries:
    def __init__(self):
        self.countries = []
        
    def add(self, text):
        text = text.replace('&nbsp;', '')
        result = re.search('(.*) \((\d+)\)', text)
        if result:
            name = result.group(1).strip()
            cnt = int(result.group(2))
            #print "'{0}', {1}".format(name, cnt)
            self.countries.append(Country(name, cnt))
            
    def sort(self):
        self.countries.sort(key=operator.attrgetter("cnt"), reverse=True)
      
  
class Country:
    def __init__(self, name, cnt):
        self.name = name
        self.cnt = cnt
        
    def __str__(self):
        return "{0} {1}".format(self.name, self.cnt)
    
    def get_gif(self):
        return self.name.replace(' ', '_')


class HtmlWriter:
    def __init__(self, countries):
        self.countries = countries
        
    def print_file(self, html_file):
        f = open(html_file, 'r')
        for line in f:
            print line,
        f.close()
        
    def print_body(self):
        if len(self.countries.countries) == 0:
            print 'Please <a href="{login}">login</a> to the Project Euler site and re-generate this page.'.format(login=LOGIN)
            return
        
        # else
        
        pos = 0
        for country in self.countries.countries:
            pos += 1
            print """<li style="float:left;margin-right:5px;width:16em;height:1.5em;">
<div style="font-size:82%;">
<a href="index.php?section=scores&amp;country={country}" style="text-decoration:none;"><img src="http://projecteuler.net/images/flags/{country_gif}.gif" alt="{country}" style="border:1px solid #bbb;vertical-align:middle;" />
&nbsp;[{pos}] {country} ({cnt})</a></div>
</li>""".format(pos=pos, country=country.name, country_gif=country.get_gif(), cnt=country.cnt)
        
    def start(self):
        old_stdout = sys.stdout
        sys.stdout = open(OUTPUT, 'w')
        
        self.print_file(HEADER1)
        print "<h3>The countries are ordered by absolute strength.</h3><br>"
        self.print_file(HEADER2)
        self.print_body()
        self.print_file(FOOTER)
        
        sys.stdout = old_stdout


def main():
    countries = Countries()
    
    text = web.get_page_with_cookies(URL)
    soup = BeautifulSoup(text)
    for tag in soup.findAll('a', href=True):
        if 'country=' in tag['href']:
            countries.add(tag.text)
            
    countries.sort()
    
    html = HtmlWriter(countries)
    html.start()
    
    webbrowser.open_new_tab(OUTPUT)
    
#############################################################################
    
if __name__ == "__main__":
    main()