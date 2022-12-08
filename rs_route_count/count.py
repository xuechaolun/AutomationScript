import re


def calc(data_list, flag):  # 第二个参数只能是1或者2！(“1”指的是rs1,“2”指的是rs2)
    temp_list = list()
    if str(flag) == '1':
        try:
            for d in data_list:
                d1 = d.split('\t')[0]
                d2 = d.split('\t')[1]
                total = len(d2.split(','))
                temp_list.append(f'{d1}\t{total}\n')
        except:
            print('1')

    elif str(flag) == '2':
        try:
            for d in data_list:
                d1 = d.split('\t')[0]
                d2 = d.split('\t')[1]
                num = re.findall(r"(\d+)\[", d2)[0]
                total = len(d2.split(',')) + int(num) - 1
                temp_list.append(f'{d1}\t{total}\n')
        except:
            print('2')
    else:
        print('第二个参数只能是1或者2！(“1”指的是rs1,“2”指的是rs2)')
        exit(-1)
    return temp_list


if __name__ == '__main__':
    rs = input('统计 rs1 文件就输入 1，统计 rs2 文件就输入 2：')
    with open('rs.txt', 'r', encoding='utf-8') as fr:
        with open('result.txt', 'w', encoding='utf-8') as fw:
            fw.writelines(sorted(calc(fr.readlines(), rs), key=lambda x: int(x.split('\t')[1]), reverse=True))
