import re
import requests
from random import getrandbits
from ipaddress import IPv4Address


from decimal import Decimal
import time

def check():
    # IP = result.IP

    # IP = '103.71.153.246'
    # IP = '103.71.153.246'

    bits = getrandbits(32) # generates an integer with 32 random bits
    addr = IPv4Address(bits) # IPv4Address object from those bits
    IP = str(addr)

    time_start = Decimal(time.time())
    # IP void doesnt have and API so I am using a post request and
    # go through the reply for the relevant information
    url = "http://www.ipvoid.com/ip-blacklist-check/"
    headers = {"Content-Type": "application/x-www-form-urlencoded",
               "Referer":"http://www.ipvoid.com/ip-blacklist-check/",}
    data = {'ip':IP}
    r = requests.post(url, headers=headers, data=data)
    content = r.content
    blacklisted = re.search(r'Blacklist Status</td><td><span.+>(\w.+)</span>', content)

    # status = blacklisted
    # print blacklisted.group(1)
    # if blacklisted.group(1) == "BLACKLISTED":
    #     detection = re.search(r'Detection Ratio</td><td>(\d+ / \d+) \(<font', resp.text)
    #     print('Detection Ratio was {0}'.format(detection.group(1)))
                # detected_sites = re.findall(r'Favicon" />(.+?)</td><td><img src=".+?" alt="Alert" title="Detected!".+?"nofollow" href="(.+?)" title', resp.text)
                # tdata = [['Site', 'Link']]
                # for site in detected_sites:
                #     tdata.append([site[0].strip(), site[1].strip()])
                # self.table(tdata, True)

    time_end = Decimal(time.time())
    return time_end - time_start

TOTAL = 0
n = 100
highest = 0
lowest = 0
for x in range(0, n):
    print x
    c = check()
    TOTAL += c
    if c > highest:
        highest = c
    if c < lowest:
        lowest = c

print 'highest ' + str(highest)
print 'lowest ' + str(lowest)
print 'average ' + str(TOTAL / n)
print 'total ' + str(TOTAL)
