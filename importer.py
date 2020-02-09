import os
import time
import Classes
import datetime
from base import Session

pastelist = []

directory = r'Raw/'
for filename in os.listdir(directory):

    paste = Classes.Paste()

    timestamp = os.path.getmtime(directory + filename)

    try:
        content = open(directory + filename, 'r', encoding='utf-8').read()
    except Exception as e:
        pass

    filename = filename.replace('.txt','')

    paste.created_at = datetime.datetime.fromtimestamp(timestamp)
    paste.href = '/raw/' + filename[-8:]
    paste.name = 'Untitled'
    paste.language = ''
    
    paste.content = content

    pastelist.append(paste)

session = Session()

session.bulk_save_objects(pastelist)

session.commit()
session.close()