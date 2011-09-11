#!/usr/bin/env python

"""
Analyze the statistics page of Project Euler (http://projecteuler.net/index.php?section=statistics)
and make a new stat. page where the countries are sorted by strength.

A country is considered to be strong if it has lots of participants.

Usage:
======
First visit the stat. page with Firefox. Since you will have to log in to the PE
site for that, the necessary cookies will be stored in Firefox's cookies.sqlite file.
This script will have to use those cookies in order to fetch the stat. page. 

./countries.py [-a | -r]    # absolute or relative strength

The output will be written to 'stat.html' by default.
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

from population.population import countries_and_population

import jabbapylib.web.web as web
from BeautifulSoup import BeautifulSoup
from optparse import OptionParser


class Countries:
    def __init__(self, options):
        self.countries = []
        self.options = options
        
    def add(self, text):
        text = text.replace('&nbsp;', '')
        result = re.search('(.*) \((\d+)\)', text)
        if result:
            name = result.group(1).strip()
            cnt = int(result.group(2))
            #print "'{0}', {1}".format(name, cnt)
            self.countries.append(Country(name, cnt))
            
    def sort(self):
        if self.options.absolute:
            self.countries.sort(key=operator.attrgetter("cnt"), reverse=True)
        else:   # if self.options.relative
            self.countries.sort(key=operator.methodcaller("relative_participation"), reverse=True)
        
    def debug(self):
        for c in self.countries:
            print >>sys.stderr, c
      
  
class Country:
    def __init__(self, name, cnt):
        self.name = name
        self.cnt = cnt
        self.population = countries_and_population[name]
        
    def __str__(self):
        return "name={0}, cnt={1}, population={2}, rel_part={3:.4f}".format(self.name, self.cnt, self.population, self.relative_participation())
    
    def get_gif(self):
        return self.name.replace(' ', '_')
    
    def relative_participation(self):
        return float(self.cnt) / float(self.population) * 100000


class HtmlWriter:
    def __init__(self, countries):
        self.countries = countries
        self.options = countries.options
        
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
            if self.options.absolute:
                print """<li style="float:left;margin-right:5px;width:16em;height:1.5em;">
<div style="font-size:82%;">
<a href="http://projecteuler.net/index.php?section=scores&amp;country={country}" style="text-decoration:none;"><img src="http://projecteuler.net/images/flags/{country_gif}.gif" alt="{country}" style="border:1px solid #bbb;vertical-align:middle;" />
&nbsp;[{pos}] {country} ({cnt})</a></div>
</li>""".format(pos=pos, country=country.name, country_gif=country.get_gif(), cnt=country.cnt)
            else:   # if self.options.relative:
                print """<li style="float:left;margin-right:5px;width:16em;height:1.5em;">
<div style="font-size:75%;">
<a href="http://projecteuler.net/index.php?section=scores&amp;country={country}" style="text-decoration:none;"><img src="http://projecteuler.net/images/flags/{country_gif}.gif" alt="{country}" style="border:1px solid #bbb;vertical-align:middle;" />
&nbsp;[{pos}] {country} ({rel_part:.3f})</a></div>
</li>""".format(pos=pos, country=country.name, country_gif=country.get_gif(), rel_part=country.relative_participation())

    def print_abs_or_rel(self):
        if self.options.absolute:
            print "<h3>The countries are ordered by absolute strength.</h3><br>"
        else:   # if self.options.relative:
            print "<h3>The countries are ordered by relative strength.</h3>"
            print """<p>The relative strength is calculated the following way: participants / population * 100000. That is, the relative
strength shows how many people participate in Project Euler out of 100,000 people.</p><br>"""
        
    def start(self):
        old_stdout = sys.stdout
        sys.stdout = open(OUTPUT, 'w')
        
        self.print_file(HEADER1)
        self.print_abs_or_rel()
        self.print_file(HEADER2)
        self.print_body()
        self.print_file(FOOTER)
        
        sys.stdout = old_stdout


def proccess_arguments():
    parser = OptionParser(usage='%prog [options]')
    
    #[options]
    parser.add_option('-a',
                      '--absolute',
                      action='store_true',
                      default=False,
                      help='Order countries by absolute strength.')
    parser.add_option('-r',
                      '--relative',
                      action='store_true',
                      default=False,
                      help='Order countries by relative strength.')

    options, arguments = parser.parse_args()
    if not options.absolute and not options.relative:
        print >>sys.stderr, "{0}: choose an option (absolute or relative). Help: -h.".format(sys.argv[0])
        sys.exit(1)
        
    if options.absolute and options.relative:
        print >>sys.stderr, "{0}: choose just one option. Help: -h.".format(sys.argv[0])
        sys.exit(1)
        
    # else
    return options

def main():
    options = proccess_arguments()
    
    countries = Countries(options)
    
    text = web.get_page_with_cookies_using_cookiejar(URL)
    soup = BeautifulSoup(text)
    for tag in soup.findAll('a', href=True):
        if 'country=' in tag['href']:
            countries.add(tag.text)
            
    countries.sort()
    
    #countries.debug()
    
    html = HtmlWriter(countries)
    html.start()
    
    webbrowser.open_new_tab(OUTPUT)
    
#############################################################################
    
if __name__ == "__main__":
    main()