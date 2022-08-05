ip = '.'.join(['{:0>3d}'.format(int(i)) for i in input('输入要拆分的ip段：').split('.')[:3]]) + '.'
country = input('输入国家：')
province = input('输入省份：')
city = input('输入城市：')
isp = input('输入运营商：')
col = input('运营商所在列? 4 or 5 :')
label = input('输入最后一列备注内容：')
n = input('按几拆分? 1 or 2 or 4 or 8 or 16 or ... ')
f = open('.\\text_c.txt', 'w', encoding='utf-8')

n1 = 0
n2 = n1 + int(n) - 1

while n2 <= 255:
    if col == '4':
        s = ip + '{:0>3d}'.format(n1) + '\t' + ip + '{:0>3d}'.format(n2) + '\t' + country + '\t' + province + '\t' + city + '\t' + isp + '\t' + '*' + '\t' + '*' + '\t' + label
    elif col == '5':
        s = ip + '{:0>3d}'.format(n1) + '\t' + ip + '{:0>3d}'.format(n2) + '\t' + country + '\t' + province + '\t' + city + '\t' + '*' + '\t' + isp + '\t' + '*' + '\t' + label
    else:
        print('列数输入有误')
        exit(1)
    f.write(s + '\n')
    n1 = n2 + 1
    n2 = n1 + int(n) - 1

f.close()
