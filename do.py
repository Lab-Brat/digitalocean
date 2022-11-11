import pathlib
import requests
import configparser


main_dir = pathlib.Path(__file__).parent.resolve()
config = configparser.ConfigParser()
config.read(f'{main_dir}/api_key.ini')
key = config['api_key']['key']

def get_request(url):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {key}"
    }

    response = requests.get(url, headers=headers)
    return response.json()

def process_ips(ips_dict):
    ips = []
    for i in ips_dict['droplets']:
        networks = i['networks']['v4']
        ips.extend([net['ip_address'] for net in networks
                        if net['type'] == 'public'])
    return ips


if __name__ == '__main__':
    url_resips = "https://api.digitalocean.com/v2/droplets"
    ips = process_ips(get_request(url_resips))
    for ip in ips:
        print(ip)
