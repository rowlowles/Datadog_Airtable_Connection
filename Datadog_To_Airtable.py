from datadog import api, initialize
from airtable import airtable
import re
import time

content = [line.rstrip('\n') for line in open('api_keys.txt')]
key_list = {}
for keys in content:
    identifier = re.search('[\w]*[\w]', keys).group()
    key = keys[re.search('[\w]*[\w][\s=]*[\s=]', keys).end():]
    key_list[identifier] = key

table_names = [line.rstrip('\n') for line in open('table_names.txt')]

options = {'api_key': key_list['Datadog_api'], 'app_key': key_list['Datadog_app']}
initialize(**options)

at = airtable.Airtable(key_list['Base_key'], key_list['Airtable_api'])

def query_stream():
    end_time = time.time()
    start_time = end_time-60
    event_stream = api.Event.query(start = start_time, end = end_time)['events']
    for event in event_stream:
        if event_stream[event]['alert_type'] == 'Error' and 'Airtable' in event_stream[event]['text']:
            at.create(table_names['Datadog Table'])

def main():
    while 1:
        query_stream()


if __name__ == "__main__":
    main()
