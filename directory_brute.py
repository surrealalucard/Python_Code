#!/usr/bin/env python

import os
import sys
import argparse
try:
    import requests
    from colorama import Fore
except ImportError:
    print('''Please Install Dependancies
               1. requests
               2. colorama                ''')


def parset():
    parser = argparse.ArgumentParser(description='A Brute Forcer of Directories',
                                     usage='%(prog)s <URLBASE> <WORDLIST> [options]')
    parser.add_argument('URLBase', help='The URL base to use.', type=str)
    parser.add_argument('Wordlist', help='Wordlist to use.', type=list)
    parser.add_argument('-x', help="Test for extension (ex .php, .html)", type=str)
    parser.add_argument('-m', default='GET', metavar='[GET, HEAD]', help='The HTTP Method to use for the request',
                        type=str)
    return parser


def brute_dirs(url, wordlist):
    req_dict = {'\n\nurl': 'Status Code'}
    for word in wordlist:
        new_url = url + "/" + word
        req = requests.get(new_url)
        stat_code = req.status_code
        #print(new_url)
        #print(stat_code)
        req_dict.update({new_url: stat_code})
        print_requests(new_url, req_dict)
    return req_dict


def print_requests(key, req_dict):
    if req_dict[key] == 200:
        print(Fore.GREEN + '{}|{} Good'.format(key, req_dict[key]))
        #print(Fore.GREEN + '{} | {} Good'.format(key, req_dict[key]))
    elif req_dict[key] == 403:
        print(Fore.MAGENTA + '{} | {} Not Authorized'.format(key, req_dict[key]))
        #print(Fore.LIGHTRED_EX + '{} | {} Not Authorized'.format(key, req_dict[key]))
    elif req_dict[key] == 404:
        pass
        #print(Fore.RED + '{}|{} Not Authorized'.format(key, req_dict[key]))
        #print(Fore.LIGHTRED_EX + '{} | {} Not Authorized'.format(key, req_dict[key]))



def main():
    parser = parset()
    if len(sys.argv) < 3:
        help = parser.print_help()
        input()
        sys.exit()


    # Get args

    args = vars(parser.parse_args())

    # Set URLBase arg as url

    url = args['URLBase']
    if 'http://' not in url:
        url = 'http://' + url

    # Set Wordlist arg as wordlist & convert to a string
    os.system('clear')
    print("Generating Wordlist")
    wordlist_dir = args['Wordlist']
    wordlist_dir = ''.join(wordlist_dir)

    # Verify wordlist file exist, and open it
    try:
        file_ds = open(wordlist_dir, 'r')
    except FileNotFoundError:
        print("File does not exist")
        #print("File does not exist")
        sys.exit(0)

    # Do actual brute forcing
    print("Starting Brute Forcing")
    directory_dict = brute_dirs(url, file_ds)

    #input('\n\nFinished, press enter to exit')
    sys.exit(0)

if (__name__=="__main__"):

    main()

#[TODO] 1.Add Threading, 2.Recursion, 3.Extensions
