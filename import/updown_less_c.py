import requests


class UpDownLessC:
    def __init__(self, route, location):
        self.route = route
        self.location = location
        self.ips = list()
        self.url = "https://status.ipip.net/updown.php?ip=" + self.route + "&level=4&a=apiv2"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0',
        }
        self.response = requests.get(url=self.url, headers=self.headers)

    def get_downstream_hop(self):
        data_json = self.response.json()
        downstream_hop = data_json['DOWNSTREAM_HOP']
        for i in downstream_hop:
            for j in i.values():
                for k in j:
                    for l in k:
                        if l == self.location:
                            self.ips.extend(k[l])

    def get_transfered_destip_unreach(self):
        data_json = self.response.json()
        transfered_destip_unreach = data_json['TRANSFERED_DESTIP_UNREACH']
        for i in transfered_destip_unreach:
            if i == self.location:
                self.ips.extend(transfered_destip_unreach[i])

    def save_file(self):
        with open('data.txt', 'w', encoding='utf-8') as fw:
            for ip in self.ips:
                fw.write(ip + '\n')

    def run(self):
        self.get_downstream_hop()
        self.get_transfered_destip_unreach()
        self.save_file()

    def __del__(self):
        self.response.close()


if __name__ == '__main__':
    # 参数1：路由
    rou = input('路由：')
    # 参数2：需要保存ip的地理位置
    loc = input('位置：')
    UpDownLessC(rou, loc).run()
