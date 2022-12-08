import os
import time

from import_location import MYDATA_PATH, ip2long, long2ip
from import_location import mydata02, mydata03, mydata04, mydata05, mydata06, mydata07, mydata08, mydata09


if __name__ == '__main__':
    TOTAL = 0
    INSERT_COUNT = 0
    FAILURE_COUNT = 0
    insert_data_dict = dict()

    print()
    print("正在导入...")

    start_time = time.time()

    with open('data.txt', 'r', encoding='utf-8') as f_data:
        for ip_list in f_data:
            TOTAL += 1
            ip_long_start = ip2long(ip_list.split('\t')[0])
            ip_long_end = ip2long(ip_list.split('\t')[1].split('\n')[0])
            if ip_long_start < mydata02:
                path1 = MYDATA_PATH + 'mydata01.txt'
            elif ip_long_start < mydata03:
                path1 = MYDATA_PATH + 'mydata02.txt'
            elif ip_long_start < mydata04:
                path1 = MYDATA_PATH + 'mydata03.txt'
            elif ip_long_start < mydata05:
                path1 = MYDATA_PATH + 'mydata04.txt'
            elif ip_long_start < mydata06:
                path1 = MYDATA_PATH + 'mydata05.txt'
            elif ip_long_start < mydata07:
                path1 = MYDATA_PATH + 'mydata06.txt'
            elif ip_long_start < mydata08:
                path1 = MYDATA_PATH + 'mydata07.txt'
            elif ip_long_start < mydata09:
                path1 = MYDATA_PATH + 'mydata08.txt'
            else:
                path1 = MYDATA_PATH + 'mydata09.txt'
            with open(path1, 'r', encoding='utf-8') as f2:
                for d2 in f2:
                    d2 = d2.split('\t')
                    if len(d2) != 9:
                        continue
                    ip_start = ip2long(d2[0])
                    ip_end = ip2long(d2[1])
                    ss = '\t' + '\t'.join(ip_list.split('\t')[2:])
                    sr = '\t'.join(d2[2:])
                    if ip_start == ip_long_start and ip_end == ip_long_end:
                        d3 = long2ip(ip_long_start) + '\t' + long2ip(ip_long_end) + ss
                        insert_data_dict[d3] = '\t'.join(d2)
                        break
                    elif ip_start == ip_long_start and ip_end > ip_long_end:
                        d3 = long2ip(ip_long_start) + '\t' + long2ip(ip_long_end) + ss
                        d3_2 = long2ip(ip_long_end + 1) + '\t' + d2[1] + '\t' + sr
                        insert_data_dict[d3 + d3_2] = '\t'.join(d2)
                        break
                    elif ip_start < ip_long_start and ip_end > ip_long_end:
                        d3_1 = d2[0] + '\t' + long2ip(ip_long_start - 1) + '\t' + sr
                        d3 = long2ip(ip_long_start) + '\t' + long2ip(ip_long_end) + ss
                        d3_2 = long2ip(ip_long_end + 1) + '\t' + d2[1] + '\t' + sr
                        insert_data_dict[d3_1 + d3 + d3_2] = '\t'.join(d2)
                        break
                    elif ip_start < ip_long_start and ip_end == ip_long_end:
                        d3_1 = d2[0] + '\t' + long2ip(ip_long_start - 1) + '\t' + sr
                        d3 = long2ip(ip_long_start) + '\t' + long2ip(ip_long_end) + ss
                        insert_data_dict[d3_1 + d3] = '\t'.join(d2)
                        break
                    else:
                        print('手动改,写入失败的行')
                        print(d2)
                        print()

    insert_data_list = sorted(insert_data_dict.items(), key=lambda x: x[1])

    jj = 0
    with open('failure1.txt', 'w', encoding='utf-8') as fww:
        for insert_data in insert_data_list:
            cc = 0
            for insert_data1 in insert_data_list[jj:]:
                if insert_data[1] == insert_data1[1]:
                    cc += 1
            if cc >= 2:
                fww.write(insert_data[0] + '\n')
            jj += 1

    insert_data_dict1 = {insert_data[1]: insert_data[0] for insert_data in insert_data_list}
    insert_data_list1 = sorted(insert_data_dict1.items(), key=lambda x: x[0])
    with open(MYDATA_PATH + 'mydata.edit.txt', 'r', encoding='utf-8') as fr1:
        with open(MYDATA_PATH + 'mydata.edit.temp.txt', 'w', encoding='utf-8') as fw1:
            index = 0
            insert_data_list_count = len(insert_data_list1)
            for dd in fr1:
                if dd == insert_data_list1[index][0]:
                    fw1.write(insert_data_list1[index][1])
                    index += 1
                    INSERT_COUNT += 1
                    if index == insert_data_list_count:
                        index -= 1
                else:
                    fw1.write(dd)


    os.remove(MYDATA_PATH + 'mydata.edit.txt')
    os.rename(MYDATA_PATH + 'mydata.edit.temp.txt', MYDATA_PATH + 'mydata.edit.txt')

    FAILURE_COUNT = TOTAL - INSERT_COUNT

    end_time = time.time()

    print(f'\n需要导入{TOTAL}条IP段\n')
    print(f'导入{INSERT_COUNT}条')
    print(f'失败{FAILURE_COUNT}条')
    print(f'\n用时{end_time - start_time:.2f}s\n')
