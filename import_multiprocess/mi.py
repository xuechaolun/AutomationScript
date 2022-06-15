import time


class B:
    mydata01 = 0
    mydata02 = 536870912
    mydata03 = 1073741824
    mydata04 = 1342177280
    mydata05 = 1610612736
    mydata06 = 2147483648
    mydata07 = 2684354560
    mydata08 = 3221225472
    mydata09 = 3758096384

    MYDATA_PATH = 'C:\\TianTexin\\framework\\library\\ip\\'

    ip2long = lambda x: sum([256 ** j * int(i) for j, i in enumerate(x.split('.')[::-1])])
    long2ip = lambda x: '.'.join(['{:0>3d}'.format(x // (256 ** i) % 256) for i in range(3, -1, -1)])

    def make_insert_data_dict(self, args):
        d_data = args[0]
        country = args[1]
        state = args[2]
        city = args[3]
        t = time.time()
        insert_data_dict = dict()
        for ip_list in d_data:
            with open('errors' + str(t) + '.txt', 'w', encoding='utf-8') as fw:
                ip_long_start = B.ip2long(ip_list.split('\t')[0])
                ip_long_end = B.ip2long(ip_list.split('\t')[1].split('\n')[0])
                if ip_long_start < B.mydata02:
                    path1 = B.MYDATA_PATH + 'mydata01.txt'
                elif ip_long_start < B.mydata03:
                    path1 = B.MYDATA_PATH + 'mydata02.txt'
                elif ip_long_start < B.mydata04:
                    path1 = B.MYDATA_PATH + 'mydata03.txt'
                elif ip_long_start < B.mydata05:
                    path1 = B.MYDATA_PATH + 'mydata04.txt'
                elif ip_long_start < B.mydata06:
                    path1 = B.MYDATA_PATH + 'mydata05.txt'
                elif ip_long_start < B.mydata07:
                    path1 = B.MYDATA_PATH + 'mydata06.txt'
                elif ip_long_start < B.mydata08:
                    path1 = B.MYDATA_PATH + 'mydata07.txt'
                elif ip_long_start < B.mydata09:
                    path1 = B.MYDATA_PATH + 'mydata08.txt'
                else:
                    path1 = B.MYDATA_PATH + 'mydata09.txt'
                with open(path1, 'r', encoding='utf-8') as f2:
                    flag = 0
                    for d2 in f2:
                        d2 = d2.split('\t')
                        if len(d2) != 9:
                            continue
                        ip_start = B.ip2long(d2[0])
                        ip_end = B.ip2long(d2[1])
                        ss = '\t' + country + '\t' + state + '\t' + city + '\t' + d2[5] + '\t' + d2[6] + '\t' + d2[7] + '\t' + d2[8]
                        sr = '\t'.join(d2[2:])
                        if ip_start == ip_long_start and ip_end == ip_long_end:
                            d3 = B.long2ip(ip_long_start) + '\t' + B.long2ip(ip_long_end) + ss
                            insert_data_dict[d3] = '\t'.join(d2)
                            flag += 1
                            break
                        elif ip_start == ip_long_start and ip_end > ip_long_end:
                            d3 = B.long2ip(ip_long_start) + '\t' + B.long2ip(ip_long_end) + ss
                            d3_2 = B.long2ip(ip_long_end + 1) + '\t' + d2[1] + '\t' + sr
                            insert_data_dict[d3 + d3_2] = '\t'.join(d2)
                            flag += 1
                            break
                        elif ip_start < ip_long_start and ip_end > ip_long_end:
                            d3_1 = d2[0] + '\t' + B.long2ip(ip_long_start - 1) + '\t' + sr
                            d3 = B.long2ip(ip_long_start) + '\t' + B.long2ip(ip_long_end) + ss
                            d3_2 = B.long2ip(ip_long_end + 1) + '\t' + d2[1] + '\t' + sr
                            insert_data_dict[d3_1 + d3 + d3_2] = '\t'.join(d2)
                            flag += 1
                            break
                        elif ip_start < ip_long_start and ip_end == ip_long_end:
                            d3_1 = d2[0] + '\t' + B.long2ip(ip_long_start - 1) + '\t' + sr
                            d3 = B.long2ip(ip_long_start) + '\t' + B.long2ip(ip_long_end) + ss
                            insert_data_dict[d3_1 + d3] = '\t'.join(d2)
                            flag += 1
                            break
                        elif ip_start > ip_long_start and ip_end == ip_long_end:
                            fw.write(
                                B.long2ip(ip_long_start) + '\t' + B.long2ip(ip_long_end) + '\t这个IP段很奇怪，需要手动处理。1\n\n')
                            flag += 1
                            break
                        elif ip_start == ip_long_start and ip_end < ip_long_end:
                            fw.write(
                                B.long2ip(ip_long_start) + '\t' + B.long2ip(ip_long_end) + '\t这个IP段被拆开标了，需要手动处理。\n\n')
                            flag += 1
                            break
                    if flag == 0:
                        fw.write(B.long2ip(ip_long_start) + '\t' + B.long2ip(ip_long_end) + '\t这个IP段很奇怪，需要手动处理。2\n\n')
        return insert_data_dict
