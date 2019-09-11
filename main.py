import requests
from bs4 import BeautifulSoup
from urllib2 import urlopen, Request

# number of proxies to rip off sslproxy.com
proxiesToRip = 20


# scrapes proxies
def scrape():

    # opens the file in append mode
    file = open(r"/Users/keith/Desktop/scraped/proxies.txt", "a+")

    # creates ip and port lists
    ip = []
    port = []

    # gets sslprxoies.com and makes sure its been scraped correctly
    page = requests.get("https://www.sslproxies.org/")
    if page.status_code == 200:
        print("@@@ SUCCESSFULLY SCRAPED @@@")
    else:
        print("@@@ ERROR @@@")

    # parses the scraped site and gets the required info
    soup = BeautifulSoup(page.content, 'html.parser')
    arrayOfRows = soup.find_all("tr")

    # pulls ip and port out of the parsed data
    for i in range(1, proxiesToRip):

        # gets ip and port and appends them to their respective lists
        ip.append(arrayOfRows[i].find_all("td")[0].get_text())
        port.append(arrayOfRows[i].find_all("td")[1].get_text())

        # writes ip + : + port to text file
        file.write(ip[i-1] + ":" + port[i-1] + "\n")

        # prints list of scraped ips to console
        print(ip[i-1])

    file.close()


# checks proxies
def check():

    #starts
    print("@@@ CHECKING PROXIES @@@")

    # opens same text file as above in read-only mode
    proxyfile = open("/Users/keith/Desktop/scraped/proxies.txt", "r")
    readProxies = proxyfile.readlines()

    # deletes duplicate proxies
    readProxies = list(set(readProxies))
    proxyfile.close()

    # keeps track of all, good, and bad proxies in list
    countGood = 0
    countBad = 0
    count = 0

    # loops through proxy list
    for j in readProxies:

        # gets ip and port from each line in txt file
        colon = j.find(":")
        ip = j[:colon]
        port = j[colon+1:]

        # creates a new Request and sets the proxy to one from the list; icanhazip.com check the ip
        req = Request('http://icanhazip.com')
        req.set_proxy(ip + ':' + port, 'http')

        # tries to connect to the website (req), if so prints proxy is verified
        try:
            my_ip = urlopen(req).read().decode('utf8')
            print("verified: " + str(ip) + " #" + str(count))
            countGood += 1
        # otherwise clears proxy and prints that its junk
        except:
            readProxies[count] = ""
            print("junk: " + str(ip) + " #" + str(count))
            countBad += 1
        count += 1

    # deletes all data in text file
    deleteData = open(r"/Users/keith/Desktop/scraped/proxies.txt", "w+")
    deleteData.write("")
    deleteData.close()

    # appends checked verfied proxies in txt file
    for q in readProxies:
        endProxyFile = open(r"/Users/keith/Desktop/scraped/proxies.txt", "a+")
        endProxyFile.write(q)
        endProxyFile.close()

    # prints how many verified and how many junk proxies total
    print(str(countGood) + " VERIFIED PROXIES")
    print(str(countBad) + " JUNK PROXIES")


# main
def main():
    scrape()
    check()


# calls main
main()

