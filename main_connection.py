from datadog import api, initialize
import re
from airtable import airtable



content = [line.rstrip('\n') for line in open('api_keys.txt')]
key_list = {}
for keys in content:
    identifier = re.search('[\w]*[\w]',keys).group()
    key = keys[re.search('[\w]*[\w][\s=]*[\s=]', keys).end():]
    key_list[identifier] = key

table_names = [line.rstrip('\n') for line in open('table_names.txt')]

options = {'api_key': key_list['Datadog_api'],'app_key':key_list['Datadog_app']}
initialize(**options)

at = airtable.Airtable(key_list['Base_Key'],key_list['Airtable_api'])



def checkUpdates():
    for table in table_names:
        at.get(table)



def main():
    checkUpdates()


if __name__ == "__main__":
    main()

