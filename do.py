import pathlib
import requests
import configparser


class DO():
    def __init__(self):
        self.mypath = pathlib.Path(__file__).parent.resolve()
        self.config = configparser.ConfigParser()
        self.config.read(f'{self.mypath}/api_key.ini')  
        self.droplets = self.get_request()['droplets']
        self.total_vm = self.get_request()['meta']['total']

    def get_request(self):
        key = self.config['api_key']['key']
        url = 'https://api.digitalocean.com/v2/droplets'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {key}'
        }

        response = requests.get(url, headers=headers)
        return response.json()

    def get_ips(self):
        ips = []
        for i in self.droplets:
            networks = i['networks']['v4']
            ips.extend([net['ip_address'] for net in networks
                            if net['type'] == 'public'])
        return ips


if __name__ == '__main__':
    do = DO()
    print(do.get_ips())
