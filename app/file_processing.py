import csv
import pandas
import datetime
import validation
import result as r
from Tkinter import Tk
from termcolor import colored, cprint


def write_file(in_fname, results):
    # This figures out the directory the file came from
    # in order to write the results to the same directory
    fname = in_fname.split('/')
    out_fname = ''
    for directory in fname[:-1]:
        out_fname += directory + '/'
    out_fname += datetime.datetime.now().strftime("%Y_%b_%d-%Hh%Mm%Ss-OSINT_Result.csv")

    print_fname('Writing', out_fname)
    with open(out_fname, 'w') as csvfile:
        resultswriter = csv.writer(csvfile)

        resultswriter.writerow(r.get_osint_headers())
        resultswriter.writerow(r.get_headers())
        for result in results:
            resultswriter.writerow(result.get_values())



def read_file(fname, mode):
    print_fname('Reading', fname)
    logs = []
    reader = csv.DictReader(open(fname, 'rb'))
    for line in reader:
        logs.append(line)
    print 'Mode: {0}'.format(mode)


    IP_addresses = []
    for log in logs:
        address = log.get(mode)
        if validation.is_valid_ip_address(address):
            #print address
            IP_addresses.append(address)

    IP_addresses = list(set(IP_addresses))
    #print IP_addresses
    number_ips = len(IP_addresses)
    print '{0} IPs found in file'.format(colored(number_ips, 'magenta', attrs=['bold']))
    return IP_addresses

def get_fname():
    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    fname = askopenfilename()

    # fname = '/home/mzhindon/share/test2.csv' # Hard coded  file for debugging

    return fname

def print_fname(reading_or_writing, fname):
    print '{0} {1}'.format(colored(reading_or_writing, 'green', attrs=['bold']), fname)

def print_results(results):
    print('\nResults')
    for result in results:
        IP = result.IP
        score = result.scoreAbuseIPDB

        #Color formating
        IP = colored(IP, 'white', attrs=['bold'])

        if(score == 0):
            score = colored(score, 'green')
        elif(score < 25):
            score = colored(score, 'yellow')
        else:
            score = colored(score, 'red')

        print('{0}: {1}'.format(IP, score))
