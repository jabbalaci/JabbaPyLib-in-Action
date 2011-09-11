#!/usr/bin/env python

"""
For test purposes.
"""

import re
import json
import operator
import jabbapylib.web.web as web
from BeautifulSoup import BeautifulSoup


URL = 'https://secure.wikimedia.org/wikipedia/en/wiki/List_of_countries_by_population'


class Countries:
    def __init__(self):
        self.countries = []
        
    def add(self, name, population):
        self.countries.append(Country(name, population))
            
    def sort(self):
        self.countries.sort(key=operator.attrgetter("name"), reverse=False)

class Country:
    def __init__(self, name, population):
        self.name = name
        self.population = population
        
    def __str__(self):
        return "{0} {1}".format(self.name, self.population)

def main():
    text = web.get_page(URL)
    soup = BeautifulSoup(text)
    
    countries = Countries()
    
    for row in soup.findAll('tr'):
        cols = row.findAll('td')
        if cols:
            rank = cols[0].text
            if rank and re.search('^\d+$', rank):
                country = cols[1].find('a', title=True).text
                population = int(cols[2].text.replace(',', ''))  
                #print country,':',population
                countries.add(country, population)
                
    countries.sort()
    
    d = {}
    for country in countries.countries:
        d[country.name] = country.population
        
    print json.dumps(d)
        
        
#############################################################################
    
if __name__ == "__main__":
    main()