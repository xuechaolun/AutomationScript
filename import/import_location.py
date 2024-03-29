import os
import re
import time


# # 这里输入要写入的地理位置
# COUNTRY = '巴西'
# STATE = '圣保罗州'
# CITY = '圣保罗'
# # CIDR默认是24
# CIDR = '32'
#
# if CIDR == '':
#     CIDR = '24'


ip2long = lambda x: sum([256 ** j * int(i) for j, i in enumerate(x.split('.')[::-1])])
long2ip = lambda x: '.'.join(['{:0>3d}'.format(x // (256 ** i) % 256) for i in range(3, -1, -1)])

MYDATA_PATH = 'C:\\TianTexin\\framework\\library\\ip\\'

mydata02 = 536870912
mydata03 = 1073741824
mydata04 = 1342177280
mydata05 = 1610612736
mydata06 = 2147483648
mydata07 = 2684354560
mydata08 = 3221225472
mydata09 = 3758096384


def main(COUNTRY, STATE, CITY, CIDR):
    TOTAL = 0
    ERROR_COUNT = 0
    INSERT_COUNT = 0
    FAILURE_COUNT = 0

    insert_data_dict = dict()

    if len(COUNTRY) == 0 or len(STATE) == 0 or len(CITY) == 0:
        print('\n国家|州|城市 无效\n')
        exit(1)

    print("正在写入...")

    start_time = time.time()

    with open('data.txt', 'r', encoding='utf-8') as fr:
        pattern = r'(((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})(\.((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})){3})'
        data = sorted(set(['.'.join([f'{int(j):0>3d}' for j in i[0].split('.')]) for i in
                           re.findall(pattern, fr.read().strip())]))
        with open('updown1.txt', 'w', encoding='utf-8') as f1:
            for d in data:
                first_ip = ip2long(d) & (-1 << (32 - int(CIDR)))
                last_ip = first_ip + 2 ** (32 - int(CIDR)) - 1
                f1.write(long2ip(first_ip) + '\t' + long2ip(last_ip) + '\n')  # cidr

    with open('updown1.txt', 'r', encoding='utf-8') as f:
        with open('updown1-1.txt', 'w', encoding='utf-8') as f1:
            for d in sorted(set(f.readlines())):
                f1.write(d)

    with open('updown1-1.txt', 'r', encoding='utf-8') as f:
        with open('updown2.txt', 'w', encoding='utf-8') as f1:
            d = f.readline()
            while d:
                current_line = d
                next_line = f.readline()
                if next_line == '':
                    f1.write(d)
                    break
                c_right = current_line.split('\t')[1].split('\n')[0]
                n_left = next_line.split('\t')[0]
                if ip2long(c_right) + 1 == ip2long(n_left):
                    next_line = current_line.split('\t')[0] + '\t' + next_line.split('\t')[1]
                else:
                    f1.write(d)
                d = next_line

    with open('updown2.txt', 'r', encoding='utf-8') as f_data:
        with open('error.txt', 'w', encoding='utf-8') as fww:
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
                    flag = 0
                    for d2 in f2:
                        d2 = d2.split('\t')
                        if len(d2) != 9:
                            continue
                        ip_start = ip2long(d2[0])
                        ip_end = ip2long(d2[1])
                        ss = '\t' + COUNTRY + '\t' + STATE + '\t' + CITY + '\t' + d2[5] + '\t' + d2[6] + '\t' + d2[
                            7] + '\t' + d2[8]
                        sr = '\t'.join(d2[2:])
                        if ip_start == ip_long_start and ip_end == ip_long_end:
                            d3 = long2ip(ip_long_start) + '\t' + long2ip(ip_long_end) + ss
                            insert_data_dict[d3] = '\t'.join(d2)
                            flag += 1
                            break
                        elif ip_start == ip_long_start and ip_end > ip_long_end:
                            d3 = long2ip(ip_long_start) + '\t' + long2ip(ip_long_end) + ss
                            d3_2 = long2ip(ip_long_end + 1) + '\t' + d2[1] + '\t' + sr
                            insert_data_dict[d3 + d3_2] = '\t'.join(d2)
                            flag += 1
                            break
                        elif ip_start < ip_long_start and ip_end > ip_long_end:
                            d3_1 = d2[0] + '\t' + long2ip(ip_long_start - 1) + '\t' + sr
                            d3 = long2ip(ip_long_start) + '\t' + long2ip(ip_long_end) + ss
                            d3_2 = long2ip(ip_long_end + 1) + '\t' + d2[1] + '\t' + sr
                            insert_data_dict[d3_1 + d3 + d3_2] = '\t'.join(d2)
                            flag += 1
                            break
                        elif ip_start < ip_long_start and ip_end == ip_long_end:
                            d3_1 = d2[0] + '\t' + long2ip(ip_long_start - 1) + '\t' + sr
                            d3 = long2ip(ip_long_start) + '\t' + long2ip(ip_long_end) + ss
                            insert_data_dict[d3_1 + d3] = '\t'.join(d2)
                            flag += 1
                            break
                        elif ip_start > ip_long_start and ip_end == ip_long_end:
                            fww.write(
                                long2ip(ip_long_start) + '\t' + long2ip(ip_long_end) + '\t这个IP段很奇怪，需要手动处理1\n\n')
                            ERROR_COUNT += 1
                            flag += 1
                            break
                        elif ip_start == ip_long_start and ip_end < ip_long_end:
                            fww.write(long2ip(ip_long_start) + '\t' + long2ip(
                                ip_long_end) + '\t这个IP段被拆开标了，需要手动处理\n\n')
                            ERROR_COUNT += 1
                            flag += 1
                            break
                    if flag == 0:
                        fww.write(
                            long2ip(ip_long_start) + '\t' + long2ip(ip_long_end) + '\t这个IP段很奇怪，需要手动处理2\n\n')
                        ERROR_COUNT += 1

    os.remove('updown1.txt')
    os.remove('updown2.txt')
    os.remove('updown1-1.txt')

    if len(insert_data_dict) == 0:
        end_time = time.time()
        print(f'\n合并后需要导入{TOTAL}条IP段\n')
        print(f'导入{INSERT_COUNT}条')
        print(f'失败{FAILURE_COUNT}条')
        print(f'异常{ERROR_COUNT}条')
        print(f'\n本次用时{end_time - start_time:.2f}s\n')
        if ERROR_COUNT != 0:
            print(f'error.txt 文本中异常的IP段需要手动修改\n')
        elif os.path.exists('error.txt'):
            os.remove('error.txt')
        if FAILURE_COUNT != 0:
            print(f'failure.txt 文本中导入失败的IP段需要再次执行 import_failure 脚本')
        elif os.path.exists('failure.txt'):
            os.remove('failure.txt')
        return FAILURE_COUNT
        # exit(1)

    insert_data_list = sorted(insert_data_dict.items(), key=lambda x: x[1])

    jj = 0
    with open('failure.txt', 'w', encoding='utf-8') as fw3:
        for insert_data in insert_data_list:
            cc = 0
            for insert_data1 in insert_data_list[jj:]:
                if insert_data[1] == insert_data1[1]:
                    cc += 1
            if cc >= 2:
                fw3.write(insert_data[0] + '\n')
            jj += 1

    insert_data_dict1 = {insert_data[1]: insert_data[0] for insert_data in insert_data_list}
    insert_data_list1 = sorted(insert_data_dict1.items(), key=lambda x: x[0])

    with open(MYDATA_PATH + 'mydata.edit.txt', 'r', encoding='utf-8') as fr1:
        with open(MYDATA_PATH + 'mydata.edit.temp.txt', 'w', encoding='utf-8') as fw1:
            index = 0
            insert_data_list_count = len(insert_data_list1)
            INSERT_COUNT = insert_data_list_count
            for dd in fr1:
                if dd == insert_data_list1[index][0]:
                    fw1.write(insert_data_list1[index][1])
                    index += 1
                    if index == insert_data_list_count:
                        index -= 1
                else:
                    fw1.write(dd)

    os.remove(MYDATA_PATH + 'mydata.edit.txt')
    os.rename(MYDATA_PATH + 'mydata.edit.temp.txt', MYDATA_PATH + 'mydata.edit.txt')

    FAILURE_COUNT = TOTAL - INSERT_COUNT - ERROR_COUNT

    end_time = time.time()

    print(f'\n合并后需要导入{TOTAL}条IP段\n')
    print(f'导入{INSERT_COUNT}条')
    print(f'失败{FAILURE_COUNT}条')
    print(f'异常{ERROR_COUNT}条')
    print(f'\n本次用时{end_time - start_time:.2f}s\n')
    if ERROR_COUNT != 0:
        print(f'error.txt 文本中异常的IP段需要手动修改\n')
    elif os.path.exists('error.txt'):
        os.remove('error.txt')
    if FAILURE_COUNT != 0:
        print(f'failure.txt 文本中导入失败的IP段需要再次执行 import_failure 脚本')
    else:
        if os.path.exists('failure.txt'):
            os.remove('failure.txt')
        if os.path.exists('failure_line.txt'):
            os.remove('failure_line.txt')
    return FAILURE_COUNT

