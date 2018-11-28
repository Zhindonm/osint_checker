#!/usr/bin/python
import re
import csv
import sys
import json
import time
import codecs
import pandas
import socket
import argparse
import datetime
import requests
import ipaddress
from IPy import IP
from Tkinter import Tk
from decimal import Decimal
from operator import itemgetter
from termcolor import colored, cprint
from tkFileDialog import askopenfilename

api_key_abuseIPDB = 'not_set_yet'
results_abuseIPDB = []
IPS = []
days = '365'
mode = 'IP Address (Impacted)'
impacted_or_origin = 'Origin'

def set_mode(option):
    global mode
    if option=='-I':
        impacted_or_origin = 'Impacted'
    else:
        impacted_or_origin = 'Origin'
    mode = 'IP Address ({0})'.format(impacted_or_origin)

def set_api_keys():
    # with open(fname) as f:
    #     content = f.read().splitlines()
    fname = './api_keys'
    with open(fname) as f_in:
        lines = filter(None, (line.rstrip() for line in f_in))

    # set and find abuseIPDB api key
    global api_key_abuseIPDB
    api_key_abuseIPDB = lines[0]
    api_key_abuseIPDB = api_key_abuseIPDB[api_key_abuseIPDB.find('\'')+1:len(api_key_abuseIPDB)-1]


def print_start_checking(flag_abuseIPDB):
    if flag_abuseIPDB:
        print '{0} to check {1}'.format(colored('Starting', 'yellow', attrs=['bold']), colored('AbuseIPDB', 'white', attrs=['bold']))


def print_done_checking(flag_abuseIPDB):
    if flag_abuseIPDB:
        print '{0} checking {1}'.format(colored('Done', 'green', attrs=['bold']), colored('AbuseIPDB', 'white', attrs=['bold']))


def check_IPs(flag_abuseIPDB):
    global IPS
    global results_abuseIPDB

    if not IPS:
        print 'File is empty. No IPs to check.'

    else:
        # AbuseIPDB check
        print_start_checking(flag_abuseIPDB)

        for IP in IPS:
            if flag_abuseIPDB:
                check_abuseIPDB(IP, days)

        print_done_checking(flag_abuseIPDB)
        results_abuseIPDB = sorted(results_abuseIPDB, key=itemgetter('Score'), reverse=True)
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
        #print 'sleeping for ' + str(time_to_wait)
        #print time_to_wait
        time.sleep(time_to_wait)
        #print 'done sleeping'


def get_category(num):
    return {
        3: 'Frad_Orders',
        4: 'DDoS_Attack',
        5: 'FTP_Brute-Force',
        6: 'Ping of Death',
        7: 'Phishing',
        8: 'Fraud VoIP',
        9: 'Open_Proxy',
        10: 'Web_Spam',
        11: 'Email_Spam',
        12: 'Blog_Spam',
        13: 'VPN IP',
        14: 'Port_Scan',
        15: 'Hacking',
        16: 'SQL Injection',
        17: 'Spoofing',
        18: 'Brute_Force',
        19: 'Bad_Web_Bot',
        20: 'Exploited_Host',
        21: 'Web_App_Attack',
        22: 'SSH',
        23: 'IoT_Targeted',}.get(num)


def check_abuseIPDB(IP, days):
    global results_abuseIPDB

    # Request stuff
    time_start = time.time()
    #print time_start
    request = 'https://www.abuseipdb.com/check/%s/json?key=%s&days=%s' % (IP, api_key_abuseIPDB, days)
    #print request
    r = requests.get(request)
    #print time_end
    #Debug API request
    #print(request)
    c = 0
    data = r.json()
    categories = {
        'Frad_Orders' : 0,
        'DDoS_Attack' : 0,
        'FTP_Brute-Force' : 0,
        'Ping of Death' : 0,
        'Phishing' : 0,
        'Fraud VoIP' : 0,
        'Open_Proxy' : 0,
        'Web_Spam' : 0,
        'Email_Spam' : 0,
        'Blog_Spam' : 0,
        'VPN IP' : 0,
        'Port_Scan' : 0,
        'Hacking' : 0,
        'SQL Injection' : 0,
        'Spoofing' : 0,
        'Brute_Force' : 0,
        'Bad_Web_Bot' : 0,
        'Exploited_Host' : 0,
        'Web_App_Attack' : 0,
        'SSH' : 0,
        'IoT_Targeted' : 0,}

    if not data:
        ip = IP
        ctg = categories
        earliestReport = 'NA'
        latestReport = 'NA'
        country = 'NA'
        isoCode = 'NA'
        isWhitelisted = False
        score = 0
        numOfReports = 0


    elif type(data) is list:
        #If is list there are multiple reports for now I am using the most recent one
        #results_abuseIPDB.append(data[0])

        #Some implementation to read more records
        #print '\n'
        #print IP
        for record in data:
            cats = record.get('category')
            for num in cats:
                category = get_category(num)
                #print category
                categories[category] +=  1

        ip = IP
        ctg = categories
        earliestReport = data[-1].get('created')
        latestReport = data[0].get('created')
        country = data[0].get('country')
        isoCode = data[0].get('isoCode')
        isWhitelisted = data[0].get('isWhitelisted')
        score = data[0].get('abuseConfidenceScore')
        numOfReports = len(data)


    else:
        cats = data.get('category')
        for num in cats:
            category = get_category(num)
            #print category
            categories[category] +=  1

        ip = IP
        ctg = categories
        earliestReport = data.get('created')
        latestReport = data.get('created')
        country =  data.get('country')
        isoCode = data.get('isoCode')
        isWhitelisted = data.get('isWhitelisted')
        score = data.get('abuseConfidenceScore')
        numOfReports = 1


    results_abuseIPDB.append({
                    'IP Address': IP,
                    'Categories': ctg,
                    'Earliest Report': earliestReport,
                    'Latest Report': latestReport,
                    'Country': country,
                    'ISO Code': isoCode,
                    'Is White listed': isWhitelisted,
                    'Score': score,
                    'Number of Reports': numOfReports})

    check_timeout(time_start)


def print_results():
    global results_abuseIPDB
    results_abuseIPDB = sorted(results_abuseIPDB, key=itemgetter('abuseConfidenceScore'), reverse=True)

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
        #print result #prints the whole dictionary per IP

def is_valid_ip_address(address):
    try:
        socket.inet_aton(address)

    except socket.error:
        return False

    return IP(address).iptype()=='PUBLIC'


def write_file(in_fname):
    fname = in_fname.split('/')
    out_fname = ''
    for directory in fname[:-1]:
        out_fname += directory + '/'
    out_fname += datetime.datetime.now().strftime("%Y_%b_%d-%Hh%Mm%Ss-OSINT_Result.csv")
    print out_fname
    pandas.DataFrame(results_abuseIPDB).to_csv(out_fname, index=False)


def read_file(fname):
    set_mode(sys.argv[1])

    logs = []
    reader = csv.DictReader(open(fname, 'rb'))
    for line in reader:
        logs.append(line)
    print 'Mode: {0}'.format(mode)

    global IPS
    for log in logs:
        address = log.get(mode)
        if is_valid_ip_address(address):
            #print address
            IPS.append(address)

    IPS = list(set(IPS))
    #print IPS
    number_ips = len(IPS)
    colored(number_ips, 'magenta', attrs=['bold'])
    print '{0} IPs found in file'.format(number_ips)


def basic_error_handling():
    if (len(sys.argv) < 2):
        print("Missing argument use -O or -I to choose between Origin or Impacted")
        return False

    return True


def main():
    #IP = '49.204.223.197'
    #days = '365'
    print sys.argv[1]
    time_start_program = Decimal(time.time())

    set_api_keys()
    #print api_key_abuseIPDB

    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    fname = askopenfilename()

    #fname = '/home/mzhindon/share/test.csv'
    print fname

    #read_file(fname)
    read_file(fname)
    flag_abuseIPDB = True
    check_IPs(flag_abuseIPDB)
    write_file(fname)
    time_end_program = Decimal(time.time())
    #print time_end_program - time_start_program


if __name__ == '__main__':
    if(basic_error_handling()):
        main()
