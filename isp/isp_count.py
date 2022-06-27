import os

import openpyxl

ip2long = lambda x: sum([256 ** j * int(i) for j, i in enumerate(x.split('.')[::-1])])

# ISP = 'telefonica'
ISP = input("input isp domain:").strip()
FILE = 'temp.txt'
COUNTRY_TOTAL = 0
STATE_TOTAL = 0
CITY_TOTAL = 0
COUNTRY_COUNT = dict()
STATE_COUNT = dict()
CITY_COUNT = dict()


def get_isp_file(isp):
    mydata_path = r'C:\TianTexin\framework\library\ip\mydata.edit.txt'
    with open(mydata_path, 'r', encoding='utf-8') as fr:
        with open(FILE, 'w', encoding='utf-8') as fw:
            for d in fr:
                d_list = d.split('\t')
                if len(d_list) != 9:
                    continue
                if isp in d_list[5] or isp in d_list[6]:
                    fw.write(d)


def countries():
    with open(FILE, 'r', encoding='utf-8') as fr:
        for i in fr:
            i_list = i.split('\t')
            if len(i_list) != 9:
                continue
            COUNTRY_COUNT[i_list[2]] = 0
            STATE_COUNT[i_list[2]] = 0
            CITY_COUNT[i_list[2]] = 0


def count():
    with open(FILE, 'r', encoding='utf-8') as fr:
        for i in fr:
            i_list = i.split('\t')
            if len(i_list) != 9:
                continue
            calc = ip2long(i_list[1]) - ip2long(i_list[0]) + 1
            global COUNTRY_TOTAL, STATE_TOTAL, CITY_TOTAL
            COUNTRY_TOTAL += calc
            COUNTRY_COUNT[i_list[2]] += calc
            if i_list[3] != '*' and i_list[2] != i_list[3]:
                STATE_TOTAL += calc
                STATE_COUNT[i_list[2]] += calc
            if i_list[4] != '*':
                CITY_TOTAL += calc
                CITY_COUNT[i_list[2]] += calc


def save():
    with open(ISP+'.txt', 'w', encoding='utf-8') as fw:
        fw.write('\t'.join(['国家', '全部', '州', '比例', '城市', '比例', '\n']))
        for country, state, city in zip(COUNTRY_COUNT.items(), STATE_COUNT.items(), CITY_COUNT.items()):
            fw.write('\t'.join([country[0], str(country[1]), str(state[1]),
                                '{:.2%}'.format(state[1] / country[1]), str(city[1]),
                                '{:.2%}'.format(city[1] / country[1]), '\n']))
        fw.write('\t'.join(['总计', str(COUNTRY_TOTAL), str(STATE_TOTAL),
                            '{:.2%}'.format(STATE_TOTAL / COUNTRY_TOTAL),
                            str(CITY_TOTAL), '{:.2%}'.format(CITY_TOTAL / COUNTRY_TOTAL), '\n']))


def save_to_excel():
    work = openpyxl.Workbook()
    worksheet1 = work.active
    worksheet1.append(['国家', '全部', '州', '比例', '城市', '比例'])
    for country, state, city in zip(COUNTRY_COUNT.items(), STATE_COUNT.items(), CITY_COUNT.items()):
        insert = [country[0], country[1], state[1],
                  ('{:.2%}'.format(state[1] / country[1])), city[1],
                  ('{:.2%}'.format(city[1] / country[1]))]
        worksheet1.append(insert)
    worksheet1.append(['总计', COUNTRY_TOTAL, STATE_TOTAL,
                       ('{:.2%}'.format(STATE_TOTAL / COUNTRY_TOTAL)),
                       CITY_TOTAL, ('{:.2%}'.format(CITY_TOTAL / COUNTRY_TOTAL))])
    work.save(ISP+'.xlsx')


def clear_file():
    os.remove('temp.txt')


get_isp_file(ISP)
countries()
count()
save_to_excel()
clear_file()
