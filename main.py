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
import os
from threading import Thread

ip_addresses = []

async def __getContentAsStringFromInOneSession(session, url: str):
    proxyUrl = getRandomProxyAsyncHttps()
    async with session.get(url,proxy=proxyUrl) as resp:
        html = await resp.text()
        return html.replace('\r\n', '').replace('\n', '')

async def __getContentAsStringFrom(url: str):
    async with aiohttp.ClientSession() as session:
        while True:
            try:
                return await __getContentAsStringFromInOneSession(session, url)
            except Exception as e:
                pass

def getRandomProxy():
    global ip_addresses

    proxy_index = random.randint(0, len(ip_addresses) - 1)
    proxy = {"http": ip_addresses[proxy_index], "https": ip_addresses[proxy_index]}

    return proxy

def getRandomProxyAsyncHttps():
    global ip_addresses

    proxy_index = random.randint(0, len(ip_addresses) - 1)
    proxy = 'https://' + ip_addresses[proxy_index]

    return proxy

async def GetLatestPastes():
    pastebins = []

    succeeded = False

    while succeeded is False:
        try:

            proxy = getRandomProxy()
            
            r = requests.get("https://pastebin.com/archive", proxies=proxy, timeout=4)
            html = r.text

            parsed_html = BeautifulSoup(html, features='html.parser')
            pastebinsMainTable_html = parsed_html.body.find('table', attrs={'class': 'maintable'})

            if pastebinsMainTable_html is not None:
                succeeded = True
        except Exception as e:
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

        #if paste['name'] == 'Untitled':
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


def downloadRAW():
    try:
        os.makedirs('Raw')
    except FileExistsError:
        pass

    with open('data.json', 'r') as f:
        savedPastebins = json.load(f)

    threads = []

    for pastebin in savedPastebins:

        if 'downloaded' in pastebin.keys():
            continue

        process = Thread(target=downloadSingleRAW, args=[pastebin, savedPastebins])
        process.start()
        threads.append(process)

        #downloadSingleRAW(pastebin,savedPastebins)
    
    for process in threads:
        process.join()

    with open('data.json', 'w') as fp:
        json.dump(savedPastebins, fp)

def downloadSingleRAW(pastebin,savedPastebins):
    succeeded = False

    while succeeded is False:
        try:

            proxy = getRandomProxy()
            
            r = requests.get("https://pastebin.com"+ pastebin['href'], proxies=proxy, timeout=4)
            html = r.text

            if 'This page has been removed!' in html:
                pastebin['downloaded'] = True
                #with open('data.json', 'w') as fp:
                #    json.dump(savedPastebins, fp)
                succeeded = True
                print('Removed')
                continue

            if 'Completing the CAPTCHA' in html or 'blocked your IP from accessing our website because we have' in html or 'resolve_captcha_headline' in html:
                raise Exception()

            with open('Raw/' + str(len(savedPastebins)) + pastebin['href'].replace('/raw/','')+'.txt', 'w', encoding='utf-8') as fp:
                fp.write('Pastename: ' + pastebin['name'] + '\r\n')
                fp.write(html)
                pastebin['downloaded'] = True
                #with open('data.json', 'w') as fp:
                #    json.dump(savedPastebins, fp)
                succeeded = True
                print('Raw ' + pastebin['href'] + ' downloaded')
                continue

        except Exception as e:
            pass

async def __main():
    global ip_addresses

    count = 0

    while(True):
        
        if count == 0:
            ip_addresses = []
            r = requests.get("https://www.proxy-list.download/api/v1/get?type=https")
            ip_addresses.extend(r.text.split('\r\n'))
            if len(ip_addresses) < 2:
                raise Exception('Unable to get proxy list')
            else:
                print('Got ' + str(len(ip_addresses)) + ' proxies')

        await GetLatestPastes()
        downloadRAW()
        #await downloadRAWAsync()
        await asyncio.sleep(10)
        count = count + 1
        if count == 20:
            count = 0

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(__main())