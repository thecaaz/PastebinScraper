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
from pastebin import PastebinAPI

headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:55.0) "
    "Gecko/20100101 Firefox/55.0"
}

async def __getContentAsStringFromInOneSession(session, url: str):
    async with session.get(url,headers=headers) as resp:
        html = await resp.text()
        return html.replace('\r\n', '').replace('\n', '')

async def __getContentAsStringFrom(url: str):
    async with aiohttp.ClientSession() as session:
        return await __getContentAsStringFromInOneSession(session, url)

async def GetLatestPastes():
    pastebins = []

    html: str = await __getContentAsStringFrom('https://pastebin.com/archive')

    if 'Scraping our site' in html:
        await asyncio.sleep(120)
        return

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
    while(True):
        await GetLatestPastes()
        await asyncio.sleep(120)

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(__main())