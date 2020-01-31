import requests
import re
import json
import asyncio
import aiohttp
import urllib.parse
from bs4 import BeautifulSoup
import datetime
import time
from typing import List
import random

proxyUrl = 'http://77.247.89.250:8080'

proxies = {
    "http": "http://103.76.253.156:3128",
    "https": "http://103.76.253.156:3128",
}

ip_addresses = []

async def __getContentAsStringFromInOneSession(session, url: str):
    async with session.get(url,headers=headers,proxy=proxyUrl) as resp:
        html = await resp.text()
        return html.replace('\r\n', '').replace('\n', '')

async def __getContentAsStringFrom(url: str):
    async with aiohttp.ClientSession() as session:
        return await __getContentAsStringFromInOneSession(session, url)

def getRandomProxy():
    global ip_addresses

    proxy_index = random.randint(0, len(ip_addresses) - 1)
    proxy = {"http": ip_addresses[proxy_index], "https": ip_addresses[proxy_index]}

    return proxy

async def GetLatestPastes():
    pastebins = []

    succeeded = False

    while succeeded is False:
        try:

            proxy = getRandomProxy()
            
            r = requests.get("https://pastebin.com/archive", proxies=proxy)
            html = r.text

            parsed_html = BeautifulSoup(html, features='html.parser')
            pastebinsMainTable_html = parsed_html.body.find('table', attrs={'class': 'maintable'})

            if pastebinsMainTable_html is not None:
                succeeded = True
        except:
            pass
    

    # html: str = await __getContentAsStringFrom('https://pastebin.com/archive')

    parsed_html = BeautifulSoup(html, features='html.parser')
    pastebinsMainTable_html = parsed_html.body.find('table', attrs={'class': 'maintable'})

    for pastebin in pastebinsMainTable_html.findAll('tr')[1:]:
        paste = {}

        index = 0

        tds = pastebin.findAll('td')

        linkTD = tds[0].findAll('a')[0]
        paste['href'] = '/raw' + linkTD.attrs['href']
        paste['name'] = linkTD.text
        
        try:
            languageTD = tds[2].findAll('a')[0]
            paste['language'] = languageTD.text
        except:
            paste['language'] = ''

        if paste['language'] == '' and paste['name'] == 'Untitled':
            pastebins.append(paste)

    savedPastebins = []

    try:
        with open('data.json', 'r') as f:
            savedPastebins = json.load(f)
    except:
        pass

    for fetchedPaste in pastebins:
        exists = False
        for savedPaste in savedPastebins:
            if fetchedPaste['href'] == savedPaste['href']:
                exists = True
                break
        if not exists:
            savedPastebins.append(fetchedPaste)

    with open('data.json', 'w') as fp:
        json.dump(savedPastebins, fp)

    print('Saved: ' + str(len(savedPastebins)))

async def __main():
    global ip_addresses

    while(True):
        
        r = requests.get("https://www.proxy-list.download/api/v1/get?type=https&anon=transparent")
        ip_addresses = r.text.split('\r\n')

        await GetLatestPastes()
        await asyncio.sleep(120)

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(__main())