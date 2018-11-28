# osint_checker

### Description

The program aims to quickly investigate a bunch of IPs using OSINT. 

It is intended to work with a csv file that contains the IP addresses you would like to check against OSINT, specifically the raw LogRhythm logs you can export from the Web Console. It will produce a csv with the results in the same directory as the input file. I highly advise to not change anything in the csv logs you get from LogRhythm since the program will validate the content to make sure only valid IP addresses are investigated and it will remove duplicates.

At this moment AbuseIPDB is implemented and I am looking into how to integrate other OSINT better.

AbuseIPDB API has a limit of 60 requests per minute which means I had to intentionally slow down requests to the minimum necessary time to prevent exceeding this (Don't worry I did the math). Additionally you can only do a maximum of 1000 requests per day.

### Requirements

If you don't have admin rights then I recommend running this from a virtual machine with a Linux guest since you will need to install dependencies. Additionally you should enable shared folders between guest and host so you can just download logs in the host, run the program from the guest, and the results will be placed in the host. I explain how to do this later.

The first step is making sure you have python. Run the following from the command line.

```
  sudo apt-get install update
  sudo apt-get install python
  sudo apt-get install python-tk
  sudo apt-get install python-pip
 ```
 
 Then change directory in the command line to the directory in which this prooject is located and type
 
 ```
 sudo pip install -r requirements.txt
 ```
 
 Finally you will need to obtain your own API key from AbuseIPDB by creating an account. Then go to your account > API Settings and here you will find your API key. Now open the file in this project named `api_keys` and replace the string `YOUR_KEY_GOES_HERE` with your key. Do not remove the ticks ( ' ) present before and after your key.
 
 ### How to use
 
 From the command line run `python osint_cheker.py -I` to check for addresses found in the **Impacted** column
 Alternatively run `python osint_cheker.py -O` to check for addresses found in the **Origin** column. Both option will open a windows to let you choose the file you would like to upload for investigation.
 
 ### Virtual Machine tips
 
 As I said before I advise to run this from a virtual machine. Make sure you have installed guest additions in order to have bidirectional clipboard, shared folders, etc. 
 
 To enable your shared folder do the following in the Host (this is for Virtual Box):
 
 1. In Virtual Box Manager > Settings > Shared Folder > Add new shared folder (little folder icon with green + icon)
 2. Choose the folder in your host that you would like to share. This folder will be refered as **foo** onwards
 3. Tick make permanent and click ok
 
 In your Guest OS you will need to create a folder and mount the Host's to the Guest's. In this example my folder in my Guest is named **bar**
 
 1. `mkdir /path/to/folder/bar`
 2. `sudo mount -t vboxsf -o rw,uid=1000,gid=1000 foo /path/to/folder/bar`
 
 Make sure you replace **foo** and **bar** with the correct names. Do not use spaces in the names unless you are more familiar with the command line.
 
 
 
