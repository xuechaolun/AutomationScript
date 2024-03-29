import os
import time

from import_location import MYDATA_PATH, ip2long, long2ip
from import_location import mydata02, mydata03, mydata04, mydata05, mydata06, mydata07, mydata08, mydata09


def main(COUNTRY, STATE, CITY):
    if not os.path.exists('failure.txt'):
        print()
        print('failure.txt 文件不存在')
        exit(1)

    with open('failure.txt', 'r', encoding='utf-8') as fr:
        if len(fr.read().strip()) == 0:
            print()
            print('failure.txt 文件中没有内容')
            exit(1)

    TOTAL = 0
    INSERT_COUNT = 0
    FAILURE_COUNT = 0
    insert_data_dict = dict()

    print("正在写入...")

    start_time = time.time()

    time.sleep(5)

    with open('failure.txt', 'r', encoding='utf-8') as fr:
        with open('failure_line.txt', 'w', encoding='utf-8') as fw:
            for frd in fr:
                if frd == '\n' or frd == '':
                    continue
                frd_list = frd.split('\t')
                if COUNTRY == frd_list[2] and STATE == frd_list[3] and CITY == frd_list[4]:
                    fw.write(frd)

    with open('failure_line.txt', 'r', encoding='utf-8') as f_data:
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
                    ss = '\t' + COUNTRY + '\t' + STATE + '\t' + CITY + '\t' + d2[5] + '\t' + d2[6] + '\t' + d2[
                        7] + '\t' + \
                         d2[8]
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

    os.remove('failure.txt')
    os.rename('failure1.txt', 'failure.txt')

    os.remove(MYDATA_PATH + 'mydata.edit.txt')
    os.rename(MYDATA_PATH + 'mydata.edit.temp.txt', MYDATA_PATH + 'mydata.edit.txt')

    FAILURE_COUNT = TOTAL - INSERT_COUNT

    end_time = time.time()

    print(f'\n合并后需要导入{TOTAL}条IP段\n')
    print(f'导入{INSERT_COUNT}条')
    print(f'失败{FAILURE_COUNT}条')
    print(f'\n本次用时{end_time - start_time:.2f}s\n')
    if FAILURE_COUNT != 0:
        print(f'failure.txt 文本中导入失败的IP段需要再次执行 import_failure 脚本')
    else:
        if os.path.exists('failure.txt'):
            os.remove('failure.txt')
        if os.path.exists('failure_line.txt'):
            os.remove('failure_line.txt')
    return FAILURE_COUNT
