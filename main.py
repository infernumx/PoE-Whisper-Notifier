import requests
import json
import threading
import time
import re
import os
import sys
from datetime import datetime
from dateutil.relativedelta import relativedelta

client_txt = r'C:\Program Files (x86)\Grinding Gear Games\Path of Exile\logs' \
             r'\client.txt'


def push_msg(title, body):
    r = requests.post(f'https://api.pushbullet.com/v2/pushes',
                      headers={
                          'Access-Token': sys.argv[1],
                          'Content-Type': 'application/json'
                      },
                      data=json.dumps({
                          'type': 'note',
                          'title': title,
                          'body': body
                      }))


cache = set()
start_time = datetime.now()

while True:
    with open(client_txt, encoding='utf-8') as f:
        for line in f.readlines()[-500:]:
            date = re.search(r'(\d+/\d+/\d+ \d+:\d+:\d+)', line).group(0)
            whisper = re.search(r'@From (.*)', line)
            if (whisper and (whisper := whisper.group(0)) and
               whisper.find('buy your') != -1):
                timestamp = datetime.strptime(date,
                                              '%Y/%m/%d %H:%M:%S')
                data = whisper + date
                if timestamp >= start_time and data not in cache:
                    print(whisper, '\n', date)
                    push_msg('PoE Whisper', f'{whisper}\n  {date}')
                    cache.add(data)
    time.sleep(1)
