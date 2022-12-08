import os
import re
import time


class MergeSameLines:
    def __init__(self):
        self.R_FILE = "C:/TianTexin/framework/library/ip/mydata.edit.txt"
        self.W_FILE = "C:/TianTexin/framework/library/ip/mydata.edit.temp.txt"
        self.fr = open(self.R_FILE, mode="r", encoding='utf-8')
        self.fw = open(self.W_FILE, mode="w", encoding='utf-8')

    ip2long = lambda x: sum([256 ** j * int(i) for j, i in enumerate(x.split('.')[::-1])])
    long2ip = lambda x: '.'.join(['{:0>3d}'.format(x // (256 ** i) % 256) for i in range(3, -1, -1)])

    # 判断相邻上下两行是否是同一个C段或B段
    @staticmethod
    def a(f, s):
        f_list = f.split('.')
        s_list = s.split('.')
        if f_list[3] != '000' or s_list[3] != '255':
            flag = 3
        else:
            flag = 2
        return True if f_list[:flag] == s_list[:flag] else False

    # 返回xxx.xxx.xxx.xxx/xx段的最后一个ip
    @staticmethod
    def b(f):
        ip_cidr = re.findall(r';##\w+##(.*?/\d+)', f)[0]
        ip = ip_cidr.split('/')[0]
        cidr = ip_cidr.split('/')[1]
        start_ip = MergeSameLines.ip2long(ip) & (-1 << (32 - int(cidr)))
        end_ip = start_ip + 2 ** (32 - int(cidr)) - 1
        return MergeSameLines.long2ip(end_ip)

    # 写入当前行，读取下一行并返回
    @staticmethod
    def c(fw, fr, s):
        fw.write(s)
        s = fr.readline()
        return s

    # 合并符合规则的上下两行
    @staticmethod
    def d(fw, fr, d1):
        d2 = fr.readline()
        d1_list = d1.split('\t')
        d2_list = d2.split('\t')
        try:
            if d1_list[2:] == d2_list[2:] and MergeSameLines.a(d1_list[0], d2_list[1]):
                d2_list[0] = d1_list[0]
            else:
                fw.write(d1)
            d1 = '\t'.join(d2_list)
        except:
            fw.write(d1)
            fw.write(d2)
            d1 = fr.readline()
        return d1

    def rename(self):
        os.remove(self.R_FILE)
        os.rename(self.W_FILE, self.R_FILE)

    def merge_country_same_lines(self, *country):
        d1 = self.fr.readline()
        while d1:
            if len(d1.split('\t')) != 9:
                d1 = MergeSameLines.c(self.fw, self.fr, d1)
                continue
            if d1.split('\t')[2] not in country:
                d1 = MergeSameLines.c(self.fw, self.fr, d1)
                continue
            if d1[:11] == ';##BACKBONE':
                end_ip = MergeSameLines.b(d1)
                d1 = MergeSameLines.c(self.fw, self.fr, d1)
                while end_ip not in d1:
                    d1 = MergeSameLines.c(self.fw, self.fr, d1)
                d1 = MergeSameLines.c(self.fw, self.fr, d1)
            elif d1[:8] == ';##DFN##' or d1[:13] == ';##REDIRECT##' or d1[:14] == ';##SATELLITE##' or d1[
                                                                                                      :8] == ';##CDN##':
                end_ip = MergeSameLines.b(d1)
                d1 = MergeSameLines.c(self.fw, self.fr, d1)
                s = time.time()
                while end_ip not in d1:
                    d1 = MergeSameLines.d(self.fw, self.fr, d1)
                    e = time.time()
                    if e - s > 0.1:
                        print(end_ip)
                        break
                d1 = MergeSameLines.c(self.fw, self.fr, d1)
            else:
                d1 = MergeSameLines.d(self.fw, self.fr, d1)

    def merge_isp_same_lines(self, col, isp, *country):
        d1 = self.fr.readline()
        while d1:
            if len(d1.split('\t')) != 9 or d1.split('\t')[2 + col - 1] != isp:
                d1 = MergeSameLines.c(self.fw, self.fr, d1)
                continue
            if 'all' not in country and d1.split('\t')[2] not in country:
                d1 = MergeSameLines.c(self.fw, self.fr, d1)
                continue
            if d1[:11] == ';##BACKBONE':
                end_ip = MergeSameLines.b(d1)
                d1 = MergeSameLines.c(self.fw, self.fr, d1)
                while end_ip not in d1:
                    d1 = MergeSameLines.c(self.fw, self.fr, d1)
                d1 = MergeSameLines.c(self.fw, self.fr, d1)
            elif d1[:8] == ';##DFN##' or d1[:13] == ';##REDIRECT##' or d1[:14] == ';##SATELLITE##' or d1[
                                                                                                      :8] == ';##CDN##':
                end_ip = MergeSameLines.b(d1)
                d1 = MergeSameLines.c(self.fw, self.fr, d1)
                s = time.time()
                while end_ip not in d1:
                    d1 = MergeSameLines.d(self.fw, self.fr, d1)
                    e = time.time()
                    if e - s > 0.1:
                        print(end_ip)
                        break
                d1 = MergeSameLines.c(self.fw, self.fr, d1)
            else:
                d1 = MergeSameLines.d(self.fw, self.fr, d1)

    def merge_all_same_lines(self):
        d1 = self.fr.readline()
        while d1:
            if d1[:11] == ';##BACKBONE':
                end_ip = MergeSameLines.b(d1)
                d1 = MergeSameLines.c(self.fw, self.fr, d1)
                while end_ip not in d1:
                    d1 = MergeSameLines.c(self.fw, self.fr, d1)
                d1 = MergeSameLines.c(self.fw, self.fr, d1)
            elif d1[:8] == ';##DFN##' or d1[:13] == ';##REDIRECT##' or d1[:14] == ';##SATELLITE##' or d1[
                                                                                                      :8] == ';##CDN##':
                end_ip = MergeSameLines.b(d1)
                d1 = MergeSameLines.c(self.fw, self.fr, d1)
                s = time.time()
                while end_ip not in d1:
                    d1 = MergeSameLines.d(self.fw, self.fr, d1)
                    e = time.time()
                    if e - s > 0.1:
                        print(end_ip)
                        break
                d1 = MergeSameLines.c(self.fw, self.fr, d1)
            elif d1[0] == ';' or d1 == '\n':
                d1 = MergeSameLines.c(self.fw, self.fr, d1)
            else:
                d1 = MergeSameLines.d(self.fw, self.fr, d1)

    def __del__(self):
        self.fr.close()
        self.fw.close()
        self.rename()


if __name__ == '__main__':
    start = time.time()
    print('合并中...')
    # MergeSameLines().merge_isp_same_lines(5, 'telefonica.com', '巴西', '法国', '英国')  # 合并第5列telefonica.com所在的巴西、法国、英国
    # MergeSameLines().merge_isp_same_lines(5, 'telefonica.com', '巴西')  # 合并第5列telefonica.com 巴西
    # MergeSameLines().merge_isp_same_lines(5, 'oi.com.br', 'all') # 合并第5列oi.com.br所在的全部国家
    # MergeSameLines().merge_country_same_lines('巴西') # 合并巴西
    MergeSameLines().merge_all_same_lines()  # 合并全部
    end = time.time()
    print(f'用时{end - start:.2f}s')
    os.system('pause')
