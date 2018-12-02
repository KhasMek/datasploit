#!/usr/bin/env python

import base
import vault
import requests
import json
import sys
from termcolor import colored
import time

ENABLED = True


class style:
    BOLD = '\033[1m'
    END = '\033[0m'


def shodandomainsearch(domain):
    time.sleep(0.3)
    endpoint = "https://api.shodan.io/shodan/host/search?key=%s&query=hostname:%s&facets={facets}" % (
        vault.get_key('shodan_api'), domain)
    req = requests.get(endpoint)
    return req.content


def banner():
    print colored(style.BOLD + '\n---> Searching in Shodan:\n' + style.END, 'blue')


def main(domain):
    if vault.get_key('shodan_api') != None:
        return json.loads(shodandomainsearch(domain))
    else:
        return [False, "INVALID_API"]


def output(data, domain=""):
    if type(data) == list and data[1] == "INVALID_API":
        print colored(
                style.BOLD + '\n[-] Shodan API Key not configured. Skipping Shodan search.\nPlease refer to http://datasploit.readthedocs.io/en/latest/apiGeneration/.\n' + style.END, 'red')
    else:
        if 'matches' in data.keys():
            for x in data['matches']:
                for key, value in x.items():
                    view = [
                        "ip_str",
                        "hostnames",
                        "domains",
                        "port",
                        "data",
                        "location"
                    ]
                    if key in view:
                        if (isinstance(value, unicode) or isinstance(value, int)):
                            if "data" in key:
                                value = value.rstrip('\n\r').replace("\n", "\n    ")
                                print("{}:".format(key))
                                print("    {}".format(value))
                            else:
                                print("{k}: {v}".format(k=key.split('_')[0], v=value))
                        elif isinstance(value, list):
                            print("{}:".format(key))
                            for i in value:
                                print("    {}".format(i))
                        elif isinstance(value, dict):
                            print("{}:".format(key.replace('_', ' ')))
                            for k, v in value.items():
                                if v:
                                    print("    {k}: {v}".format(k=k.replace('_', ' '), v=v))
                print('')
        print "-----------------------------\n"


if __name__ == "__main__":
    try:
        domain = sys.argv[1]
        banner()
        result = main(domain)
        output(result, domain)
    except Exception as e:
        print e
        print "Please provide a domain name as argument"
