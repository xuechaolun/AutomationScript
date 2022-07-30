"""
1 输入要提取的国家、运营商、运营商所在列和最后一列备注
2 将 tt 的结果复制到 text_c 中
3 读文件 text_c
4 判断 若 text_c  中的最后一列和输入的运营商一致，则提取 text_c 中的地理位置；若不一致则用输入的国家补充地理位置
5 最后的结果需保存到 text_c 中
"""

country = input('country:').strip()
isp = input('isp:').strip()
isp_col = input('isp_col(pleas input "4" or "5"):').strip()
while isp_col != '4' and isp_col != '5':
    isp_col = input('isp_col(pleas input "4" or "5"):').strip()
last_col = input('last_col:').strip() + '\n'

CONTENT = list()

with open('text_c.txt', 'r', encoding='utf-8') as fr:
    for line in fr.readlines():
        line_list = [i for i in line.split(' ') if i != '']
        line_list[0] = '.'.join([f'{int(li):0>3d}'for li in line_list[0].split('.')])
        if '\n' not in line_list[-1]:
            line_list[-1] += '\n'
        if line_list[4] == '骨干网' and line_list[6] == '骨干网':
            line_list[3] = f'{line_list[3]} {line_list[4]}'
            line_list[4] = line_list[3]
            line_list[5] = '*'
        if isp_col == '5':
            if line_list[-1] == isp + '\n':
                row = '\t'.join(
                    [line_list[0], line_list[0], line_list[3], line_list[4], line_list[5], '*', isp, '*', last_col])
                CONTENT.append(row)
            else:
                row = '\t'.join([line_list[0], line_list[0], country, country, '*', '*', isp, '*', last_col])
                CONTENT.append(row)
        elif isp_col == '4':
            if line_list[-1] == isp + '\n':
                row = '\t'.join(
                    [line_list[0], line_list[0], line_list[3], line_list[4], line_list[5], isp, '*', '*', last_col])
                CONTENT.append(row)
            else:
                row = '\t'.join([line_list[0], line_list[0], country, country, '*', isp, '*', '*', last_col])
                CONTENT.append(row)

with open('text_c.txt', 'w', encoding='utf-8') as fw:
    fw.writelines(CONTENT)
