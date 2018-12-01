import abuseIPDB as AIPDB

class Result:
    def __init__(self, IP):
        self.IP = IP
        #Abuse IPDB
        self.scoreAbuseIPDB = 0
        self.categories = {
            'Fraud_Orders' : 0,
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
        self.numOfReports = 0
        self.earliestReport = 'None'
        self.latestReport = 'None'
        self.country = 'None'
        self.isoCode = 'None'


    def __eq__(self, other):
        return self.scoreAbuseIPDB == other.scoreAbuseIPDB


    def __lt__(self, other):
        return self.scoreAbuseIPDB > other.scoreAbuseIPDB

    def get_values(self):
        values = [self.IP,
                    self.scoreAbuseIPDB,
                    self.get_non_zero_categories(),
                    self.numOfReports,
                    self.earliestReport,
                    self.latestReport,
                    self.country,
                    self.isoCode,]
        return values



    def get_non_zero_categories(self):
        non_zero_categories = {}
        # Iterate over the categories dictionary and build a dictionary
        # that has non-zero categories to remove noise in result
        for key in self.categories:
            value = self.categories[key]
            if value > 0:
                non_zero_categories[key] = value

        if not non_zero_categories:
            return 'None'
        return non_zero_categories

def test(IP):
    IP.numOfReports += 1

def get_osint_headers():
    headers = ['OSINT',]
    headers.extend(AIPDB.get_osint_headers())
    return headers

def get_headers():
    headers = ['IP',]
    headers.extend(AIPDB.get_headers())
    return headers
