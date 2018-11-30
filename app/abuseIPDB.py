import json
import requests

def get_timeout():
    return 1

# Reports in AbuseIPDB have tags that indicate what type of malicious
# activity they are being reported for. The API returns a several reports
# each one has a list of categories but they are returned as numbers so
# this is to get change that number into a string
# More information here https://www.abuseipdb.com/categories
def get_category(num):
    return {
        3: 'Fraud_Orders',
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


def check(result, days, api_key):

    IP = result.IP

    # Request stuff
    request = 'https://www.abuseipdb.com/check/%s/json?key=%s&days=%s' % (IP, api_key, days)
    #print request
    r = requests.get(request)
    data = r.json()

    if not data:
        return

    elif type(data) is list:

        # Reads all the records to compile how many reports each
        # category has
        for record in data:
            categories = record.get('category')
            for num in categories:
                category = get_category(num)
                #print category
                result.categories[category] +=  1


        score = data[0].get('abuseConfidenceScore')
        numOfReports = len(data)
        earliestReport = data[-1].get('created')
        latestReport = data[0].get('created')
        country = data[0].get('country')
        isoCode = data[0].get('isoCode')


    else:
        categories = data.get('category')
        for num in categories:
            category = get_category(num)
            #print category
            result.categories[category] +=  1


        score = data.get('abuseConfidenceScore')
        numOfReports = 1
        earliestReport = data.get('created')
        latestReport = data.get('created')
        country =  data.get('country')
        isoCode = data.get('isoCode')


    result.scoreAbuseIPDB = score
    result.numOfReports = numOfReports
    result.earliestReport = earliestReport
    result.latestReport = latestReport
    result.country = country
    result.isoCode = isoCode
