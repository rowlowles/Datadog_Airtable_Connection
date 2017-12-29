from datadog import api, initialize
from airtable import airtable
import time
import re

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

table_sizes = {}


def initial_setup():
    for table in table_names:
        current_stats = at.get(table)['records']
        table_sizes[table] = current_stats.__len__()


def check_airtable_updates():
    # Note: Airtable API is limited to 5 calls/second. Exceeding it puts a 30 sec timeout on future calls.
    # If possible, we want to avoid hitting that timeout.
    for table in table_names:
        pre_call_time = time.time()
        size = at.get(table)['records'].__len__()

        diff = size - table_sizes[table]
        if diff > 0:
            # Post to Datadog that a row was created, update the table size
            api.Event.create(title=str(diff) + " new rows in Airtable Created")
            table_sizes[table] = size

        elif diff < 0:
            # Post to Datadog that a row was deleted, update the table size
            api.Event.create(title=str(abs(diff)) + " rows in Airtable Deleted")
            table_sizes[table] = size

        else:
            pass

        post_call_time = time.time()
        while (post_call_time - pre_call_time) <= .2:
            time.sleep(.01)
            post_call_time = time.time()


def main():
    initial_setup()
    while 1:
        check_airtable_updates()


if __name__ == "__main__":
    main()
