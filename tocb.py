#!/usr/bin/env python

import sys
from jabbapylib.clipboard.clipboard import text_to_clipboards

def main():
    stuff = sys.stdin.read()
    text_to_clipboards(stuff)

#############################################################################
    
if __name__ == "__main__":
    main()