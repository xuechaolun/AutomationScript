import os
import re
import time
import multiprocessing

from mi import B


class A:
    ip2long = lambda x: sum([256 ** j * int(i) for j, i in enumerate(x.split('.')[::-1])])
    long2ip = lambda x: '.'.join(['{:0>3d}'.format(x // (256 ** i) % 256) for i in range(3, -1, -1)])

    MYDATA_PATH = 'C:\\TianTexin\\framework\\library\\ip\\'

    # 这里输入要导入的地理位置
    COUNTRY = '巴西'
    STATE = '帕拉伊巴州'
    CITY = '若昂佩索阿'
    CIDR = '30'

    if len(COUNTRY) == 0 or len(STATE) == 0 or len(CITY) == 0:
        print('\n国家|州|城市 无效')
        exit(1)
    if CIDR == '':
        CIDR = '24'
    print()
    print("正在导入...")

    TOTAL = 0
    ERROR_COUNT = 0
    INSERT_COUNT = 0
    FAILURE_COUNT = 0

    start_time = time.time()
    insert_data_dict = dict()

    @staticmethod
    def get_cidr_ips():
        with open('data.txt', 'r', encoding='utf-8') as fr:
            pattern = r'(((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})(\.((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})){3})'
            data = sorted(
                set(['.'.join([f'{int(j):0>3d}' for j in i[0].split('.')]) for i in
                     re.findall(pattern, fr.read().strip())]))
            with open('updown1.txt', 'w', encoding='utf-8') as fw:
                for d in data:
                    first_ip = A.ip2long(d) & (-1 << (32 - int(A.CIDR)))
                    last_ip = first_ip + 2 ** (32 - int(A.CIDR)) - 1
                    fw.write(A.long2ip(first_ip) + '\t' + A.long2ip(last_ip) + '\n')  # cidr

    @staticmethod
    def deduplication_sorted_ips():
        with open('updown1.txt', 'r', encoding='utf-8') as fr:
            with open('updown1-1.txt', 'w', encoding='utf-8') as fw:
                for d in sorted(set(fr.readlines())):
                    fw.write(d)

    @staticmethod
    def merge_same_lines():
        with open('updown1-1.txt', 'r', encoding='utf-8') as fr:
            with open('updown2.txt', 'w', encoding='utf-8') as fw:
                d = fr.readline()
                while d:
                    current_line = d
                    next_line = fr.readline()
                    if next_line == '':
                        fw.write(d)
                        break
                    c_right = current_line.split('\t')[1].split('\n')[0]
                    n_left = next_line.split('\t')[0]
                    if A.ip2long(c_right) + 1 == A.ip2long(n_left):
                        next_line = current_line.split('\t')[0] + '\t' + next_line.split('\t')[1]
                    else:
                        fw.write(d)
                    d = next_line

    @staticmethod
    def get_total_count():
        with open('updown2.txt', 'r', encoding='utf-8') as fr:
            A.TOTAL = len(fr.readlines())

    @staticmethod
    def get_error_count():
        with open('error.txt', 'r', encoding='utf-8') as fr:
            data = fr.read().strip()
            if '\n\n' in data:
                A.ERROR_COUNT = len(data.split('\n\n'))
            else:
                A.ERROR_COUNT = 0

    @staticmethod
    def make_insert_data_dict():
        with open('updown2.txt', 'r', encoding='utf-8') as fr:
            ip_list = fr.readlines()
            num = len(ip_list)
            cpu_count = os.cpu_count()
            task_list = list()
            if num < cpu_count:
                cpu_count = 2
                # task_list = [(ip_list[:num // 2], A.COUNTRY, A.STATE, A.CITY),
                #              (ip_list[1 * (num // 2):], A.COUNTRY, A.STATE, A.CITY), ]
            for i in range(cpu_count):
                args = (ip_list[i * (num // cpu_count):(i + 1) * (num // cpu_count)], A.COUNTRY, A.STATE, A.CITY)
                task_list.append(args)
            pool = multiprocessing.Pool(processes=cpu_count)
            result = pool.map(B().make_insert_data_dict, task_list)
            pool.close()
            pool.join()
            for res in result:
                for k in res:
                    if k != '':
                        A.insert_data_dict.update(res.items())

    @staticmethod
    def clear_error_file():
        with open('error.txt', 'w', encoding='utf-8') as fw:
            pass

    @staticmethod
    def merge_errors_file():
        with open('error.txt', 'a', encoding='utf-8') as fw:
            for e in os.listdir(os.path.dirname(__file__)):
                if 'errors' in e:
                    with open(e, 'r', encoding='utf-8') as fr:
                        fw.write(fr.read())
                    os.remove(e)

    @staticmethod
    def clear_updown_file():
        os.remove('updown1.txt')
        os.remove('updown2.txt')
        os.remove('updown1-1.txt')

    @staticmethod
    def print_insert_data_dict_is_zero():
        if len(A.insert_data_dict) == 0:
            end_time = time.time()
            print(f'\n合并后需要导入{A.TOTAL}条IP段\n')
            print(f'导入{A.INSERT_COUNT}条')
            print(f'失败{A.FAILURE_COUNT}条')
            print(f'异常{A.ERROR_COUNT}条')
            print(f'\n用时{end_time - A.start_time:.2f}s\n')
            print(f'error.txt 文本中的异常IP段需要手动修改\n')
            exit(1)

    @staticmethod
    def get_failure_file():
        insert_data_list = sorted(A.insert_data_dict.items(), key=lambda x: x[1])
        jj = 0
        with open('failure.txt', 'w', encoding='utf-8') as fw:
            for insert_data in insert_data_list:
                cc = 0
                for insert_data1 in insert_data_list[jj:]:
                    if insert_data[1] == insert_data1[1]:
                        cc += 1
                if cc >= 2:
                    fw.write(insert_data[0] + '\n')
                    A.FAILURE_COUNT += 1
                jj += 1
        return insert_data_list

    @staticmethod
    def exchange_key_value_sorted():
        insert_data_dict1 = {insert_data[1]: insert_data[0] for insert_data in A.get_failure_file()}
        insert_data_list1 = sorted(insert_data_dict1.items(), key=lambda x: x[0])
        return insert_data_list1

    @staticmethod
    def insert_data():
        with open(A.MYDATA_PATH + 'mydata.edit.txt', 'r', encoding='utf-8') as fr1:
            with open(A.MYDATA_PATH + 'mydata.edit.temp.txt', 'w', encoding='utf-8') as fw1:
                index = 0
                insert_data_list1 = A.exchange_key_value_sorted()
                insert_data_list_count = len(insert_data_list1)
                A.INSERT_COUNT = insert_data_list_count
                for dd in fr1:
                    if dd == insert_data_list1[index][0]:
                        fw1.write(insert_data_list1[index][1])
                        index += 1
                        if index == insert_data_list_count:
                            index -= 1
                    else:
                        fw1.write(dd)

    @staticmethod
    def rename_mydata_file():
        os.remove(A.MYDATA_PATH + 'mydata.edit.txt')
        os.rename(A.MYDATA_PATH + 'mydata.edit.temp.txt', A.MYDATA_PATH + 'mydata.edit.txt')

    @staticmethod
    def print_insert_data_dict_not_is_zero():
        end_time = time.time()
        print(f'\n合并后需要导入{A.TOTAL}条IP段\n')
        print(f'导入{A.INSERT_COUNT}条')
        print(f'失败{A.FAILURE_COUNT}条')
        print(f'异常{A.ERROR_COUNT}条')
        print(f'\n用时{end_time - A.start_time:.2f}s\n')
        if A.ERROR_COUNT != 0:
            print(f'error.txt 文本中异常的IP段需要手动修改\n')
        elif os.path.exists('error.txt'):
            os.remove('error.txt')
        if A.FAILURE_COUNT != 0:
            print(f'failure.txt 文本中导入失败的IP段需要再次执行 import_failure 脚本')
        elif os.path.exists('failure.txt'):
            os.remove('failure.txt')

    @staticmethod
    def run():
        A.get_cidr_ips()
        A.deduplication_sorted_ips()
        A.merge_same_lines()
        A.get_total_count()
        A.make_insert_data_dict()
        A.clear_error_file()
        A.merge_errors_file()
        A.get_error_count()
        A.print_insert_data_dict_is_zero()
        A.insert_data()
        A.rename_mydata_file()
        A.print_insert_data_dict_not_is_zero()
        A.clear_updown_file()


if __name__ == '__main__':
    A().run()
