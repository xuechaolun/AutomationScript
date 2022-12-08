import os
import re

path = r'C:\TianTexin\loveapp\dpt\module'
file_list = ['asn.config.000001_009999.php', 'asn.config.010000_019999.php', 'asn.config.020000_029999.php',
             'asn.config.030000_039999.php', 'asn.config.040000_049999.php', 'asn.config.050000_059999.php',
             'asn.config.060000_199999.php', 'asn.config.200000_399999.php', 'asn.config.400000_599999.php']

with open('as_default_config_test.txt', 'w', encoding='utf-8') as fw:
    for fl in file_list:
        with open(os.path.join(path, fl), 'r', encoding='utf-8') as fr:
            asn = fr.read()
            fw.write(asn)

with open('as_default_config_test.txt', 'r', encoding='utf-8') as fr:
    content = fr.read()
    p = r"' => \[.*?\['巴西'.*?\],"
    asn_list = re.findall(p, content, re.S)
print(len(asn_list))