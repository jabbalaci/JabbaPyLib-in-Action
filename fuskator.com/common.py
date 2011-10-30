#!/usr/bin/env python

import os

from urlparse import urlparse
from datetime import datetime

from jabbapylib.dateandtime.dateandtime import get_date_from_year_to_day


def simplify_date(s):
    year, month, day = s.split()[1:4][::-1]
    if len(day) == 1:
        day = '0' + day
    date = datetime.strptime("{yyyy} {Mmm} {dd}".format(yyyy=year, Mmm=month, dd=day), "%Y %b %d")
    template = "{year}_{month:02}_{day:02}"
    return template.format(year=date.year, month=date.month, day=date.day)


def get_subdir_name(url):
    file_name = os.path.split(urlparse(url)[2])[1]
    file_base_name= os.path.splitext(file_name)[0]
    
    tmp = os.path.split(urlparse(url)[2])
    guid = os.path.split(tmp[0])[1]
    
    return "{stamp}_{guid}_{desc}".format(stamp=get_date_from_year_to_day(), guid=guid, desc=file_base_name)

#############################################################################

if __name__ == "__main__":
    url = 'http://fuskator.com/full/lnf8cHriPBu/Caprice_hegre_solo_Super+Model_teen_tfpez_trimmed.html'
    print get_subdir_name(url)
    
    s = 'Sat, 29 Oct 2011 18:32:56 GMT'
    print simplify_date(s)