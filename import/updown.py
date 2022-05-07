import re
import time

import requests


class UpDown:
    def __init__(self, ip):
        self.url = 'https://status.ipip.net/updown.php'
        self.headers = {
            'Origin': 'https://status.ipip.net',
            'Referer': 'https://status.ipip.net/updown.php',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0',
        }
        self.form_data = {
            'flag': '0',
            'ip': str(ip),
            'rdns': '1',
            'level': '2',
        }
        self.response = requests.post(url=self.url, data=self.form_data, headers=self.headers)

    @staticmethod
    def ip2long(ip):
        return sum([256 ** int(i) * int(j) for i, j in enumerate(str(ip).split('.')[::-1])])

    @staticmethod
    def long2ip(long):
        return '.'.join(['{:0>3d}'.format(long // (256 ** i) % 256) for i in range(3, -1, -1)])

    @staticmethod
    def sort(ip_list):
        return sorted(list(set(ip_list)), key=lambda x: UpDown.ip2long(x), reverse=False)

    def get_data(self):
        data = self.response.content.decode('utf-8')
        pattern = '<span class="J_whois" style="">(.*?)</span>'
        ip_list = re.findall(pattern, data)
        return UpDown.sort(ip_list)

    def __del__(self):
        self.response.close()


if __name__ == '__main__':
    # route = '200.223.126.184'
    route = input("请输入路由：")
    start = time.time()
    ud = UpDown(route)
    with open('data.txt', 'w', encoding='utf-8') as f:
        for ip1 in ud.get_data():
            f.write(ip1 + '\n')
    end = time.time()
    print(f'用时{end - start:.2f}s')
