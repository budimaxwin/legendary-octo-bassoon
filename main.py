from ast import keyword
from email.mime import base
from urllib import response
import requests
import time
import random
from bs4 import BeautifulSoup
from threading import Thread
import logging; logging.basicConfig(level=logging.DEBUG)


def user_agent():
  fake = faker.Faker()
  useragent = fake.user_agent()
  return useragent
  
# global variable here
useragents = [
    'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)', 
    'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Mobile Safari/537.36 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
    ]
referrer = [
    'pornhub',
    'hijab indo',
    'prank ojol',
    'tante lagi sendirian'
]
bad_referer = [
    "https://google.co.id/search?q=" + random.choice(referrer).replace(" ","+"),
    "https://www.xnxx.com/search/cuan777",
    "https://xnxxcom.club/se/?query=cuan777",
    "https://www.xvideos.com/?k=cuan777"
]
routes = [
    "https://google.co.id/",
    "https://bing.com/",
    "https://yahoo.com/",
    "https://baidu.com/",
    "https://duckduckgo.com/",
    "https://id-id.facebook.com/",
    "https://line.me/",
    "https://yandex.com/"
]
temporary_proxy = []

def search_keyword(query):
    list_link  = []
    url = 'http://google.co.id/search?q=' + query + '&num=100'
    response = requests.get(url, verify=False)
    soup = BeautifulSoup(response.content, 'html.parser') 
    contents = soup.find_all('div', attrs={'class':'kCrYT'})
    for content in contents:
        link = content.find('a', href=True)
        if link != None:
           list_link.append(link['href'])

    return list_link

def check_proxy(baseurl, proxies):
    google_url = "https://www.google.co.id/"
    for proxy in proxies:
        headers = {
            'User-agent': user_agent(),
            "referer": random.choice(routes),
            "Upgrade-Insecure-Requests": "1"
        }
        proxies = {
            'http': f'http://{proxy}', 'https': f'https://{proxy}'
        }
        session = requests.Session()
        session.proxies = proxies

        try:
            r = session.get(google_url+baseurl, headers=headers, timeout=5, verify=False)
            print(r.url)
            if r.status_code == 200:
                f = open('proxy_list.txt', 'a+')
                f.write(proxy + "\n")
            else:
                pass
        except Exception as e:
            pass

        session = requests.Session()
def clark_proxy():
    proxies = requests.get(
        "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list.txt"
    )
    proxies = proxies.text.split("\n")[9:]
    proxies = [p.split(" ")[0] for p in proxies]
    return proxies

def proxy_for_you():
    proxies = []
    urls = [
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
        "https://api.proxyscrape.com/?request=getproxies&timeout=500&country=all&ssl=all&type=http&anonymity=all", 
        "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http"
    ]
    for url in urls:
            for proxy in requests.get(url).text.split('\n'):
                proxies.append(proxy.split('\n')[0].strip())
    return proxies

def counter(proxies):
    jatah_proxy = int(len(proxies) / 4)
    dividers = []
    i = 0
    for c in range(i, len(proxies), jatah_proxy):
        if i is c:
            continue
        divider = [i, c]
        dividers.append(divider)
        i+=jatah_proxy
    return dividers

def main():
    proxies = proxy_for_you()
    dividers = counter(proxies=proxies)
    keyword = "cuan777 site:beacons.ai" #input("Keyword: ")
    urls = search_keyword(keyword)
    baseurl = [
        "http://api.linkr.bio/callbacks/go?url=https://beacons.ai/cuan777",
        "https://www.google.co.id/amp/beacons.ai/cuan777"
    ]#None
    baseurl = urls[0] #random.choice(baseurl)

    #for i in range(len(urls)):
    #    print(i+1, urls[i].split("&sa")[0])
    #    i+=1

    #choice = input('Link number: ')

    #if choice.isdigit():
    #    baseurl = urls[int(choice) - 1]

    for div in dividers:
        t = []
        for i in range(div[0], div[1]):
            t.append(proxies[i])

        th = Thread(target=check_proxy, name=f"Thread {div}", kwargs={'baseurl':baseurl, 'proxies':t})
        th.start()
        t = []

if __name__=="__main__":
    print(user_agent())
    while(True):
        main()
        time.sleep(60*60)
