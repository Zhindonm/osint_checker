class Result:
    def __init__(self, IP):
        self.IP = IP
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
        self.earliestReport = 'NA'
        self.latestReport = 'NA'
        self.country = 'NA'
        self.isoCode = 'NA'


    def __eq__(self, other):
        return self.scoreAbuseIPDB == other.scoreAbuseIPDB


    def __lt__(self, other):
        return self.scoreAbuseIPDB > other.scoreAbuseIPDB

    def get_values(self):
        line = '{0},{1},{2},{3},{4},{5},{6},{7}'.format(
                            self.IP,
                            self.scoreAbuseIPDB,
                            self.get_non_zero_categories(),
                            self.numOfReports,
                            self.earliestReport,
                            self.latestReport,
                            self.country,
                            self.isoCode,)
        return line



    def get_non_zero_categories(self):
        non_zero_categories = {}
        # Iterate over the categories dictionary and build a dictionary
        # that has non-zero categories to remove noise in result
        for key in self.categories:
            value = self.categories[key]
            if value > 0:
                non_zero_categories[key] = value

        return non_zero_categories

def test(IP):
    IP.numOfReports += 1

def get_headers():
    line = '{0},{1},{2},{3},{4},{5},{6},{7}'.format(
                        "IP",
                        "Score AbuseIPDB ",
                        "Categories AbuseIPDB ",
                        "Num of reports AbuseIPDB ",
                        "First seen AbuseIPDB",
                        "Last seen AbuseIPDB",
                        "Country",
                        "isoCode",)
