import tls_client
import random
import os
import string
import sys
import requests
import time
import concurrent.futures
import json

config = json.load(open('config.json', encoding='UTF-8'))

class Joiner:
    def __init__(self) -> None:
        self.session = tls_client.Session(client_identifier='chrome112', random_tls_extension_order=True)
        self.session.proxies = self.proxy() if config['proxyless'] else None
        self.session.headers = {
            'authority': 'discord.com',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/json',
            'origin': 'https://discord.com',
            'referer': 'https://discord.com/',
            'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9016 Chrome/108.0.5359.215 Electron/22.3.12 Safari/537.36',
            'x-debug-options': 'bugReporterEnabled',
            'x-discord-locale': 'en-US',
            'x-discord-timezone': 'Europe/Stockholm',
            'x-super-properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRGlzY29yZCBDbGllbnQiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfdmVyc2lvbiI6IjEuMC45MDE2Iiwib3NfdmVyc2lvbiI6IjEwLjAuMTkwNDUiLCJvc19hcmNoIjoieDY0Iiwic3lzdGVtX2xvY2FsZSI6InN2IiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV09XNjQpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIGRpc2NvcmQvMS4wLjkwMTYgQ2hyb21lLzEwOC4wLjUzNTkuMjE1IEVsZWN0cm9uLzIyLjMuMTIgU2FmYXJpLzUzNy4zNiIsImJyb3dzZXJfdmVyc2lvbiI6IjIyLjMuMTIiLCJjbGllbnRfYnVpbGRfbnVtYmVyIjoyMTg2MDQsIm5hdGl2ZV9idWlsZF9udW1iZXIiOjM1MjM2LCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsfQ=='
        }

    @staticmethod
    def proxy():
        try:
            proxy = random.choice(open('Data/proxies.txt', 'r').readlines()).strip()
            return {'http': f'http://{proxy}', 'https': f'http://{proxy}'}
        except Exception as e:
            print(e)

    def cookies(self):
        try:
            site = self.session.get('https://discord.com')
            self.session.cookies = site.cookies
        except Exception as e:
            print(e)

    @staticmethod
    def id(length):
        try:
            return ''.join(random.sample(string.ascii_lowercase + string.digits, length))
        except Exception as e:
            print(e)

    def join(self, token, invite):
        try:
            self.session.headers['Authorization'] = token
            response = self.session.post('https://discord.com/api/v9/invites/' + invite, json={'session_id': self.id(32)})
            data = response.json()
            if response.status_code == 429:
                sleep_time = data['retry_after']
                print('Ratelimit')
                time.sleep(sleep_time)
            elif response.status_code == 401:
                print('Invalid')
            elif response.status_code == 403:
                print('Locked')
            elif response.status_code == 200:
                print('Success')
            elif 'captcha_key' in response.text:
                print('Captcha')
            else:
                print(response.text)
        except Exception as e:
            print(e)

class Thread:
    def __init__(self) -> None:
        self.thread = config['thread']

    @staticmethod
    def read_tokens1():
        list_tokens = []
        with open('Data/tokens.txt', 'r') as file:
            for line in file.readlines():
                line = line.strip()
                if ':' in line:
                    line = line.split(':')[2]
                    list_tokens.append(line)
                else:
                    list_tokens.append(line)
        return list_tokens

    def main(self):
        Start = Joiner()
        invite = input('Invite Code: ')
        start_time = time.time()
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.thread) as e:
            futures = [e.submit(Start.join, token, invite) for token in self.read_tokens1()]
            concurrent.futures.wait(futures)

        end_time = time.time()
        elapsed = end_time - start_time
        print(f'Joined in {elapsed}s')

if __name__ == "__main__":
    try:
        os.system('cls' if os.name == 'nt' else 'clear')
        Thread().main()
    except KeyboardInterrupt:
        print('Exiting...')
        time.sleep(2)
        sys.exit()