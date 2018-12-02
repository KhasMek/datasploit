#!/usr/bin/env python

import base
import sys
import whois
from termcolor import colored
import time

ENABLED = True


class style:
    BOLD = '\033[1m'
    END = '\033[0m'


def banner():
    print colored(style.BOLD + '---> Finding Whois Information.\n' + style.END, 'blue')


def main(domain):
    data = whois.whois(domain)
    for k in ('creation_date', 'expiration_date', 'updated_date'):
        if k in data:
            date = data[k][0] if isinstance(data[k], list) else data[k]
            if data[k]:
                data[k] = date.strftime('%m/%d/%Y')
    return dict(data)


def output(data, domain=""):
    for k, v in data.items():
        if isinstance(v, str):
            print("{k}: {v}".format(k=k.replace('_', ' '), v=v))
        elif isinstance(v, list):
            print("{}:".format(k.replace('_', ' ')))
            for i in v:
                print("    {}".format(i))
    print "\n-----------------------------\n"


if __name__ == "__main__":
    try:
        domain = sys.argv[1]
        banner()
        result = main(domain)
        output(result, domain)
    except Exception as e:
        print e
        print "Please provide a domain name as argument"
