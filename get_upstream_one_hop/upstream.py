import os
import random
import re
import time

import requests


class UpStream:
    def __init__(self, ip, isp):
        self.ip = ip.strip('\n')
        self.isp = isp
        self.url = 'https://status.ipip.net/updown.php'
        self.headers = {
            'Origin': 'https://status.ipip.net',
            'Referer': 'https://status.ipip.net/updown.php',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0',
        }
        self.form_data = {
            'flag': '1',
            'ip': self.ip,
            'rdns': '1',
            'level': '1',
        }
        self.response = requests.post(url=self.url, data=self.form_data, headers=self.headers)
        print(self.ip + ' start')
        print(f'status_code = {self.response.status_code}')

    def get_data(self):
        html_content = self.response.content.decode('utf-8')
        patt = r'<table.*?id="US2IP">(.*)</table>'
        data = re.findall(patt, html_content, re.S)[0]
        patt1 = r'<th><span class="J_whois">(.*?)</span>.*?\((.*?)\).*?</th>'
        data1 = re.findall(patt1, data, re.S)
        return data1

    def save(self, data):
        with open(self.isp + '_upstream.txt', 'a', encoding='utf-8') as fw:
            with open(self.isp + '_log.txt', 'a', encoding='utf-8') as fw_log:
                now_time = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
                fw_log.write(now_time + ' ' + self.ip + ' -> ' + f'status_code = {self.response.status_code}' + '\n')
                if len(data) != 0:
                    fw.write(self.ip + '\t=>\n')
                    for i in data:
                        fw.write('\t' + str(i) + '\n')
                    fw.write('\n')

    def run(self):
        self.save(self.get_data())

    def __del__(self):
        self.response.close()
        print(self.ip + ' end\n')


ip2long = lambda x: sum([256 ** j * int(i) for j, i in enumerate(x.split('.')[::-1])])
long2ip = lambda x: '.'.join(['{:0>3d}'.format(x // (256 ** i) % 256) for i in range(3, -1, -1)])


def get_em_file(isp, country):
    mydata_path = r'C:\TianTexin\framework\library\ip\mydata.edit.txt'
    with open(mydata_path, 'r', encoding='utf-8') as fr:
        with open(isp + '.txt', 'w', encoding='utf-8') as fw:
            for dd in fr:
                d_list = dd.split('\t')
                if len(d_list) != 9:
                    continue
                ip0 = d_list[0]
                ip1 = d_list[1]
                if ip0.split('.')[-1] == '000' and ip1.split('.')[-1] == '255' and (
                        d_list[5] == isp or d_list[6] == isp) and d_list[3] == country:
                    result = (ip2long(d_list[1]) - ip2long(d_list[0]) + 1) // 256
                    for ii in range(result):
                        temp = long2ip(ip2long(d_list[0]) + ii * 256)
                        fw.write(temp + '\n')


def get_last_line(file_name):
    offset = -10
    with open(file_name, 'rb') as f:  # 读取方式要以字节读取
        while 1:
            """
            f.seek(off, whence=0)：从文件中移动off个操作标记（文件指针），正往结束方向移动，负往开始方向移动。
            如果设定了whence参数，就以whence设定的起始位为准，0代表从头开始，1代表当前位置，2代表文件最末尾位置。 
            """
            f.seek(offset, 2)
            result = f.readlines()
            if len(result) > 1:  # 至少逆序读了2行
                return result[-1].decode('utf-8')
                # print(result[-1].decode('utf-8')) # 获取最后一行
                # break
            offset *= 2


def delete_scanned_lines(isp):
    last_line = get_last_line(isp + '_log.txt')
    ip = last_line.split(' ')[2]
    with open(isp + '.txt', 'r', encoding='utf-8') as fr:
        data = fr.readlines()
    with open(isp + '.txt', 'w', encoding='utf-8') as fw:
        for i, ddd in enumerate(data):
            if ddd.strip() == ip:
                try:
                    fw.writelines(data[i+1:])
                except:
                    print(f"{isp}.txt 中的ip已经扫描完毕")
                    exit(1)
                break


if __name__ == '__main__':
    # ISP = 'embratel.com.br'
    # COUNTRY = '巴西'
    ISP = input('input domain:').strip()
    COUNTRY = input('input country:').strip()
    if ISP == '' or COUNTRY == '':
        print('domain or country is empty!\nplease input domain and country.')
        os.system('pause')
        exit(1)
    if not os.path.exists(ISP + '.txt'):
        print('\n获取 ' + COUNTRY + ' ' + ISP + ' 只标注到国家的c段ip\n')
        get_em_file(ISP, COUNTRY)
    else:
        print('\n删除 '+ISP + '.txt 中'+'已扫描过的 ip\n')
        delete_scanned_lines(ISP)
    for d in open(ISP + '.txt', 'r', encoding='utf-8'):
        try:
            UpStream(d, ISP).run()
            time.sleep(random.uniform(5,6))
        except:
            with open(ISP+'_error.txt', 'a', encoding='utf-8') as fw_error:
                fw_error.write(d)
    os.system('pause')
