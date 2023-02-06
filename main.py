from ovh import Client
from json import load
from requests import get
from sys import exit, stderr
from time import sleep

try:
    with open('/app/config.json') as f:
        config = load(f)
except Exception as e:
    print(f'Config file could not be loaded!\n{e}', file=stderr)
    exit(1)

client = Client(
    endpoint='ovh-eu',               # Endpoint of API OVH Europe (List of available endpoints)
    application_key=config['application_key'],    # Application Key
    application_secret=config['application_secret'], # Application Secret
    consumer_key=config['consumer_key'],       # Consumer Key
)

domain = config['domain']
id = config['record_id']

curr_ip = client.get(f'/domain/zone/{domain}/record/{id}')['target']

while True:
    act_ip = get('https://api.ipify.org').text

    if curr_ip != act_ip:
        print(f'Detected new IP: {act_ip}, old IP: {curr_ip}')

        try:
            client.put(f'/domain/zone/{domain}/record/{id}', 
                target=act_ip
            )
        except Exception as e:
            print(f'Error while updating the IP address\n{e}', file=stderr)
        else:
            print('IP updated successfully!')

        curr_ip = act_ip

    sleep(config['check_interval'])

