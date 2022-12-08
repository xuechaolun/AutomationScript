filename = input('input filename:') + '.txt'
with open(filename, 'r', encoding='utf-8') as fr:
    with open('result.txt', 'w', encoding='utf-8') as fw:
        for line in fr:
            line_array = line.split(',')
            #        '72.224.16.60'    => 'cpe-72-224-16-60.nycap.res.rr.com',
            res = f"        '{line_array[0]}'    => '{line_array[1]}',\n"
            fw.write(res)

print('finish')
import os
os.system('pause')
