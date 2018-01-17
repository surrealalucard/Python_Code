#!/usr/bin/env python

import os
import sys
import argparse
import threading
try:
    import requests
    from colorama import Fore
except ImportError:
    print('''Please Install Dependancies
               1. requests
               2. colorama                ''')
banner = '''
.___________..______     ____    ____     __    __       ___      .______       _______   _______ .______      
|           ||   _  \    \   \  /   /    |  |  |  |     /   \     |   _  \     |       \ |   ____||   _  \     
`---|  |----`|  |_)  |    \   \/   /     |  |__|  |    /  ^  \    |  |_)  |    |  .--.  ||  |__   |  |_)  |    
    |  |     |      /      \_    _/      |   __   |   /  /_\  \   |      /     |  |  |  ||   __|  |      /     
    |  |     |  |\  \----.   |  |        |  |  |  |  /  _____  \  |  |\  \----.|  '--'  ||  |____ |  |\  \----.
    |__|     | _| `._____|   |__|        |__|  |__| /__/     \__\ | _| `._____||_______/ |_______|| _| `._____|
                                                                                                               
'''

def parset():
    parser = argparse.ArgumentParser(description='A Brute Forcer of Directories',
                                     usage='%(prog)s <URLBASE> <WORDLIST> [options]')
    parser.add_argument('URLBase', help='The URL base to use.', type=str)
    parser.add_argument('Wordlist', help='Wordlist to use.', type=list)
    parser.add_argument('-x', help="Test for extension (ex .php, .html)", type=str)
    parser.add_argument('-m', default='GET', metavar='[GET, HEAD]', help='The HTTP Method to use for the request',
                        type=str)
    parser.add_argument('-t', default='5', help='How many threads to use (default 5)', type=int)
    return parser

def get_wordcount(wordlist):
    count = 0
    for word in wordlist:
        count +=1
    return count

def brute_dirs(url, wordlist, threads, extension=None):
    req_dict = {'\n\nurl': 'Status Code'}
    i = 0
    i_max = get_wordcount(wordlist)
    for num in range(i_max):
        for thread in range(threads):
            if(i == i_max):
                return req_dict
            if(extension):
                t = threading.Thread(target=get_url, args=(url, wordlist[i], req_dict, extension))
                t.start()
            else:
                t = threading.Thread(target=get_url, args=(url, wordlist[i], req_dict, extension))
                t.start()
            i += 1
           
def get_url(url, word, req_dict, extension=None):
    new_url = url + "/" + word
    req = requests.get(new_url)
    stat_code = req.status_code
    #print(new_url)
    #print(stat_code)
    req_dict.update({new_url: stat_code})
    print_requests(new_url, req_dict)
    if(extension):
        ext_url = new_url + extension
        ext_req = requests.get(ext_url)
        ext_stat_code = ext_req.status_code
        req_dict.update({ext_url : ext_stat_code})
        print_requests(ext_url, req_dict)


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

    # Getting extension if its set

    if(args['x']):
        extension = args['x']

    # Getting number of threads
    
    threads = args['t']
 
    # Set Wordlist arg as wordlist & convert to a string
    os.system('clear')
    print(banner)
    print("Using threads {}".format(threads))
    print("Generating Wordlist")
    wordlist_dir = args['Wordlist']
    wordlist_dir = ''.join(wordlist_dir)

    # Verify wordlist file exist, and open it
    try:
        file_ds = open(wordlist_dir, 'r')
        file_ds = [line[:-1] for line in file_ds]
    except FileNotFoundError:
        print("File does not exist")
        #print("File does not exist")
        sys.exit(0)

    # Do actual brute forcing
    print("Starting Brute Forcing on {}".format(url))
    if(extension):
        req_list = brute_dirs(url, file_ds, threads, extension)
    else:
        req_list = brute_dirs(url, file_ds, threads)

    #input('\n\nFinished, press enter to exit')
    sys.exit(0)

if (__name__=="__main__"):

    main()

#[TODO] 1.Add Threading, 2.Recursion, 3.Extensions
