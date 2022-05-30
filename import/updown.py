import re
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

    def get_data(self):
        content = self.response.content.decode('utf-8')
        reachable_d_pattern = r'<table class="table table-bordered" id="REACHABLE_D">(.*?)</table>'
        unreachable_pattern = r'<table class="table table-bordered" id="UNREACHABLE">(.*?)</table>'
        reachable_d = re.findall(reachable_d_pattern, content, re.S)[0]
        unreachable = re.findall(unreachable_pattern, content, re.S)[0]
        pattern = r'<span class="J_whois" style.*?>(.*?)</span>'
        reachable_d_ips = re.findall(pattern, reachable_d)
        unreachable_ips = re.findall(pattern, unreachable)
        ips = list()
        ips.extend(reachable_d_ips)
        ips.extend(unreachable_ips)
        return ips

    def save_file(self):
        with open('data.txt', 'w', encoding='utf-8') as fw:
            for ip in self.get_data():
                fw.write(ip + '\n')

    def run(self):
        self.save_file()

    def __del__(self):
        self.response.close()


if __name__ == '__main__':
    route = input("请输入路由：")
    UpDown(route).run()
