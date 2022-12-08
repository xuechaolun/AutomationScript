import os
import time

import import_location
import import_location_failure

# 这里输入要写入的地理位置
COUNTRY = '巴西'
STATE = '圣保罗州'
CITY = '*'
# CIDR默认是24
CIDR = ''

if CIDR == '':
    CIDR = '24'

if __name__ == '__main__':
    start_time = time.time()
    print('第1次写入')
    if import_location.main(COUNTRY, STATE, CITY, CIDR) != 0:
        count = 1
        while True:
            count += 1
            print(50 * '-')
            print(f'第{count}次写入')
            if import_location_failure.main(COUNTRY, STATE, CITY) == 0:
                break
        print(f'总共写入{count}次')
    else:
        print('总共写入1次')
    if int(CIDR) > 24:
        os.system('python format_split_c.py')
    end_time = time.time()
    print(f'\n总共用时{end_time - start_time:.3f}s')
