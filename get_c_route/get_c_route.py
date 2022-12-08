import random
import re
import time

import requests

class GetCRoute:
    def __init__(self, ip):
        self.ip = ip.strip()
        self.url = 'https://status.ipip.net/updown.php'
        self.headers = {
            'Origin': 'https://status.ipip.net',
            'Referer': 'https://status.ipip.net/updown.php',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0',
        }
        self.form_data = {
            'flag': '0',
            'ip': self.ip,
            'rdns': '1',
            'level': '4',
        }
        self.response = requests.post(url=self.url, data=self.form_data, headers=self.headers)

    def is_route(self):
        html_text = self.response.content.decode('utf-8')
        # print(html_text)
        pattern = r'DOWNSTREAM_HOP(.*?)US2IP'
        pattern1 = r'>[1234]<'
        res = re.findall(pattern, html_text, re.S)[0]
        res1 = re.findall(pattern1, res, re.S)
        # print(res1)
        if '>1<' in res1 or '>2<' in res1 or '>3<'in res1 or '>4<'in res1:
            return True
            # print(11)
        else:
            return False
            # print(00)

    def __del__(self):
        self.response.close()


if __name__ == '__main__':
    ip = input('ip:')
    format_ip = '.'.join(ip.split('.')[2])+'.0'
    with open('骨干网路由.txt', 'w', encoding='utf-8') as fw:
        for i in range(256):
            format_ip = '.'.join(ip.split('.')[2]) + '.' + str(i)
            flag = GetCRoute(format_ip).is_route()
            if flag:
                fw.write(f'{format_ip}\n')
            time.sleep(random.uniform(5.0,6.0))
