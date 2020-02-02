import json
import os

savedPastebins = []
searchList = []
ignoreList = []

def saveIfNotIgnored(search,string):
    
    for ignore in ignoreList:
        ignore = ignore.replace('\n','')
        if ignore in string:
            return

    with open('RawInteresting/'+filename, 'w', encoding='utf-8') as wf:
        wf.write('Term Matched: ' +search)
        wf.write('\r\n')
        wf.write(string)
    print(filename)

if __name__ == "__main__":
    print('Starting...')
    with open('data.json', 'r') as f:
        savedPastebins = json.load(f)

    with open('searchCriteria', 'r') as f:
        searchList = f.readlines()
    with open('ignoreCriteria', 'r') as f:
        ignoreList = f.readlines()

    for pastebin in savedPastebins:
        filename = pastebin['href'].replace('/raw/','')+'.txt'
        try:
            with open('Raw/'+filename, 'r', encoding='utf-8') as f:
                string = f.read()
                for search in searchList:
                    if search in string:
                        saveIfNotIgnored(search,string)
                        break
        except Exception as e:
            pass

    print('Done')
