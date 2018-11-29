#!/usr/bin/python
import re
import csv
import sys
import time
import json
import codecs
import socket
import argparse
import requests
import ipaddress
from sys import argv
from termcolor import colored, cprint
from decimal import Decimal

api_key = ''
results_abuseIPDB = []
IPS = []
days = '365'

def check_IPs():
    if not IPS:
        print("File is empty. No IPs to check. ")

    else:
        # AbuseIPDB check
        print '{0} to check {1}'.format(colored('Starting', 'yellow', attrs=['bold']), colored('AbuseIPDB', 'white', attrs=['bold']))
        for IP in IPS:
            check_abuseIPDB(IP, days)

        print '{0} checking {1}'.format(colored('Done', 'green', attrs=['bold']), colored('AbuseIPDB', 'white', attrs=['bold']))
        #print_results()


def check_timeout(start):
    # There is a 60 requests per minute limit so this bit is to slow down
    # the number of requests per second to avoid the enforced restrictions
    # it makes sure the request always takes at least one sec
    start = Decimal(start)
    current = Decimal(time.time())
    #print current
    time_passed = current - start
    #print time_passed
    if time_passed < 1:
        time_to_wait = 1 - time_passed
        #print time_to_wait
        time.sleep(time_to_wait)


def check_abuseIPDB(IP, days):

    # Request stuff
    time_start = time.time()
    #print time_start
    request = 'https://www.abuseipdb.com/check/%s/json?key=%s&days=%s' % (IP, api_key, days)
    #print request
    r = requests.get(request)
    #print time_end
    #Debug API request
    #print(request)
    c = 0
    data = r.json()
    if not data:
        results_abuseIPDB.append({'ip': IP,
                        'category': [],
                        'created': '',
                        'country': '',
                        'isoCode': '',
                        'isWhitelisted': False,
                        'abuseConfidenceScore': 0})
    elif type(data) is list:
        #If is list there are multiple reports for now I am using the most recent one
        results_abuseIPDB.append(data[0])

        #Some implementation to read more records
        # for record in data:
        #     results_abuseIPDB.append(record)
    else:
        results_abuseIPDB.append(data)


    check_timeout(time_start)



def print_results():
    print('\nRESULTS')
    for result in results_abuseIPDB:
        IP = result.get('ip')
        score = result.get('abuseConfidenceScore')

        #Color formating
        IP = colored(IP, 'blue', attrs=['bold'])

        if(score == 0):
            score = colored(score, 'green')
        elif(score < 25):
            score = colored(score, 'yellow')
        else:
            score = colored(score, 'red')

        print('{0}: {1}'.format(IP, score))

def read_file(fname):
    # with open(fname) as f:
    #     content = f.read().splitlines()
    with open(fname) as f_in:
        lines = filter(None, (line.rstrip() for line in f_in))

    IPS.extend(lines)

    number_ips = len(IPS)
    colored(number_ips, 'magenta', attrs=['bold'])
    print '{0} IPs found in file'.format(number_ips)

def basic_error_handling():
    if (len(sys.argv) < 2):
        print("Missing argument")
        return False

    return True

def main():

    #IP = '49.204.223.197'
    #days = '365'

    time_start_program = Decimal(time.time())
    file_with_ips = sys.argv[1]
    read_file(file_with_ips)

    check_IPs()
    time_end_program = Decimal(time.time())
    print time_end_program - time_start_program


if __name__ == '__main__':
    if(basic_error_handling()):
        main()
