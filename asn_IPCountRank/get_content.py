#!/usr/bin/python3
import os

with open('as_number.txt', 'r', encoding='utf-8') as fr:
    with open('as_content.txt', 'a', encoding='utf-8') as fw:
        for d in fr:
            print(d)
            cmd = 'php /home/codebase/loveapp/dpt/toolbox/asn.php --check=3 --as=' + d.strip()
            fw.write(os.popen(cmd).read())

os.system('sz as_content.txt')
print('finish')
