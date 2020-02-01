import json
import os

savedPastebins = []
searchList = []

if __name__ == "__main__":
    print('Starting...')
    with open('data.json', 'r') as f:
        savedPastebins = json.load(f)

    with open('searchCriteria', 'r') as f:
        searchList = f.readlines()

    for pastebin in savedPastebins:
        filename = pastebin['href'].replace('/raw/','')+'.txt'
        try:
            with open('Raw/'+filename, 'r', encoding='utf-8') as f:
                string = f.read()
                for search in searchList:
                    if search in string:
                        with open('RawInteresting/'+filename, 'w', encoding='utf-8') as wf:
                            wf.write('Term Matched: ' +search)
                            wf.write('\r\n')
                            wf.write(string)
                        print(filename)
                        break
        except FileNotFoundError as e:
            pass

    print('Done')
