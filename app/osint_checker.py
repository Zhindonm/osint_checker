#!/usr/bin/python
import re
import os
import sys
import time
import codecs
import api_keys
import argparse
import ipaddress
import result as r
from Tkinter import Tk
import abuseIPDB as AIPDB
from decimal import Decimal
import file_processing as FP
from termcolor import colored, cprint
from tkFileDialog import askopenfilename

days = '365'
impacted_or_origin = 'Origin'
current_folder = os.path.dirname(__file__)

def set_mode(option):
    if option=='-I':
        impacted_or_origin = 'Impacted'
    else:
        impacted_or_origin = 'Origin'

    mode = 'IP Address ({0})'.format(impacted_or_origin)
    return mode


def set_api_keys():
    fname = current_folder + 'api_keys'
    print(current_folder)
    with open(fname) as f_in:
        lines = filter(None, (line.rstrip() for line in f_in))

    api_key = api_keys.API_KEYS()

    # set and find abuseIPDB api key
    api_key_abuseIPDB = lines[0]
    api_key_abuseIPDB = api_key_abuseIPDB[api_key_abuseIPDB.find('\'')+1:len(api_key_abuseIPDB)-1]
    api_key.abuseIPDB = api_key_abuseIPDB

    return api_key


def print_start_checking(flag_abuseIPDB):
    if flag_abuseIPDB:
        print '{0} to check {1}'.format(colored('Starting', 'yellow', attrs=['bold']), colored('AbuseIPDB', 'white', attrs=['bold']))


def print_done_checking(flag_abuseIPDB):
    if flag_abuseIPDB:
        print '{0} checking {1}'.format(colored('Done', 'green', attrs=['bold']), colored('AbuseIPDB', 'white', attrs=['bold']))


def check_IPs(IP_addresses, api_key, flag_abuseIPDB):
    results = []

    if not IP_addresses:
        print 'File is empty. No IPs to check.'

    else:
        print_start_checking(flag_abuseIPDB)

        for IP in IP_addresses:
            result = r.Result(IP)

            time_start = time.time()
            # print time_start

            if flag_abuseIPDB:
                if not AIPDB.check(result, days, api_key.abuseIPDB):
                    print '{0} your API Quota https://www.abuseipdb.com/account#api-settings'.format(colored('Check', 'red', attrs=['bold']))
                    print 'It looks like you have run out requests for today.\n'
                    return results

            results.append(result)
            check_timeout(time_start)

        print_done_checking(flag_abuseIPDB)

    results = sorted(results)
    return results


def check_timeout(start):
    # There is a 60 requests per minute limit so this bit is to slow down
    # the number of requests per second to avoid the enforced restrictions
    # it makes sure the request always takes at least one sec
    start = Decimal(start)
    current = Decimal(time.time())
    timeout_abuseIPDB = AIPDB.get_timeout()
    # print current
    time_passed = current - start
    # print time_passed

    if time_passed <= timeout_abuseIPDB:
        time_to_wait = timeout_abuseIPDB - time_passed
        #print 'sleeping for ' + str(time_to_wait)
        #print time_to_wait
        time.sleep(time_to_wait)
        #print 'done sleeping'

    # timeouts for other osint go here


def basic_error_handling():
    if (sys.argv[1] not in ['-O', '-I']):
        print("Missing argument use -O or -I to choose between Origin or Impacted")
        return False

    return True


def main():
    # days = '365'
    # print sys.argv[1]
    time_start_program = Decimal(time.time())

    api_key = api_keys.API_KEYS()
    api_key = set_api_keys()

    # fname = FP.get_fname()
    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    fname = askopenfilename()

    mode = set_mode(sys.argv[1])

    IP_addresses = FP.read_file(fname, mode)
    flag_abuseIPDB = True
    results_osint = check_IPs(IP_addresses, api_key, flag_abuseIPDB)


    # FP.print_results(results_osint)
    FP.write_file(fname, results_osint)
    time_end_program = Decimal(time.time())
    print 'Total runtime in seconds: {0}'.format(time_end_program - time_start_program)


if __name__ == '__main__':
    if(basic_error_handling()):
        main()
