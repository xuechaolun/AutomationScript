import os

with open('C:\\TianTexin\\framework\\library\\ip\\mydata.edit.txt', 'r', encoding='utf-8') as fr1:
    with open('C:\\TianTexin\\framework\\library\\ip\\mydata.edit.temp.txt', 'w', encoding='utf-8') as fw1:
        for d in fr1:
            d1 = d.split('\t')
            if len(d1) != 9:
                fw1.write(d)
                continue
            left_ip = d1[0]
            right_ip = d1[1]
            ss = '\t'.join(d1[2:])
            left_ip_list = left_ip.split('.')
            right_ip_list = right_ip.split('.')
            if left_ip_list[3] == '000' and right_ip_list[3] == '255':
                fw1.write(d)
            elif left_ip_list[3] != '000' and right_ip_list[3] != '255':
                if left_ip_list[2] == right_ip_list[2]:
                    fw1.write(d)
                else:
                    right = '.'.join([left_ip_list[0], left_ip_list[1], left_ip_list[2], '255'])
                    fw1.write(left_ip + '\t' + right + '\t' + ss)
                    if int(right_ip_list[2])-int(left_ip_list[2]) > 1:
                        mid_l = '.'.join([left_ip_list[0], left_ip_list[1], str(int(left_ip_list[2])+1), '000'])
                        mid_r = '.'.join([right_ip_list[0], right_ip_list[1], str(int(right_ip_list[2])-1), '255'])
                        fw1.write(mid_l+'\t'+mid_r+'\t'+ss)
                    left = '.'.join([right_ip_list[0], right_ip_list[1], right_ip_list[2], '000'])
                    fw1.write(left + '\t' + right_ip + '\t' + ss)
            elif left_ip_list[3] == '000' and right_ip_list[3] != '255':
                if left_ip_list[2] == right_ip_list[2]:
                    fw1.write(d)
                else:
                    right = '.'.join([right_ip_list[0], right_ip_list[1], str(int(right_ip_list[2]) - 1), '255'])
                    fw1.write(left_ip + '\t' + right + '\t' + ss)
                    left = '.'.join([right_ip_list[0], right_ip_list[1], right_ip_list[2], '000'])
                    fw1.write(left + '\t' + right_ip + '\t' + ss)
            elif left_ip_list[3] != '000' and right_ip_list[3] == '255':
                if left_ip_list[2] == right_ip_list[2]:
                    fw1.write(d)
                else:
                    right = '.'.join([left_ip_list[0], left_ip_list[1], left_ip_list[2], '255'])
                    fw1.write(left_ip + '\t' + right + '\t' + ss)
                    left = '.'.join([left_ip_list[0], left_ip_list[1], str(int(left_ip_list[2]) + 1), '000'])
                    fw1.write(left + '\t' + right_ip + '\t' + ss)
            else:
                fw1.write(d)
                print('Accident')
                print(d)

os.remove('C:\\TianTexin\\framework\\library\\ip\\mydata.edit.txt')
os.rename('C:\\TianTexin\\framework\\library\\ip\\mydata.edit.temp.txt','C:\\TianTexin\\framework\\library\\ip\\mydata.edit.txt')
