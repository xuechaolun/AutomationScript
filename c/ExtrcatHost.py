def parse(host):
    key = {
        'aju': ['巴西', '塞尔希培州', '阿拉卡茹'],
        'bhe': ['巴西', '米纳斯吉拉斯州', '贝洛奥里藏特'],
        'blm': ['巴西', '帕拉州', '贝伦'],
        'bre': ['巴西', '圣保罗州', '巴鲁埃里'],
        'bru': ['巴西', '圣保罗州', '包鲁'],
        'bsa': ['巴西', '联邦区', '巴西利亚'],
        'bva': ['巴西', '罗赖马州', '保艾佩蓝卡'],
        'cas': ['巴西', '圣保罗州', '坎皮纳斯'],
        'cba': ['巴西', '马托格罗索州', '库亚巴'],
        'cem': ['巴西', '米纳斯吉拉斯州', '康塔根'],
        'cim': ['巴西', '圣埃斯皮里图州', '伊塔佩米林河畔卡舒埃鲁'],
        'cpe': ['巴西', '南马托格罗索州', '大坎普市'],
        'cps': ['巴西', '里约热内卢州', '坎普斯'],
        'cru': ['巴西', '伯南布哥州', '卡鲁阿鲁'],
        'csl': ['巴西', '南里奥格兰德州', '南卡希亚斯'],
        'cta': ['巴西', '巴拉那州', '库里奇巴'],
        'fla': ['巴西', '塞阿腊州', '福塔莱萨'],
        'fns': ['巴西', '圣卡塔琳娜州', '弗洛里亚诺波利斯'],
        'fsa': ['巴西', '巴伊亚州', '费拉迪圣安娜'],
        'gna': ['巴西', '戈亚斯州', '戈亚尼亚'],
        'gvs': ['巴西', '米纳斯吉拉斯州', '瓦拉达里斯州长市'],
        'iai': ['巴西', '圣卡塔琳娜州', '伊塔雅伊'],
        'jfa': ['巴西', '米纳斯吉拉斯州', '茹伊斯迪福拉'],
        'jpa': ['巴西', '帕拉伊巴州', '若昂佩索阿'],
        'jve': ['巴西', '圣卡塔琳娜州', '若因维利'],
        'lda': ['巴西', '巴拉那州', '隆德里纳'],
        'lpa': ['巴西', '圣保罗州', '圣保罗'],
        'mba': ['巴西', '帕拉州', '马拉巴'],
        'mce': ['巴西', '里约热内卢州', '马卡埃'],
        'mco': ['巴西', '阿拉戈斯州', '马塞约'],
        'mga': ['巴西', '巴拉那州', '马林加'],
        'mns': ['巴西', '亚马孙州', '马瑙斯'],
        'mpa': ['巴西', '阿马帕州', '马卡帕'],
        'nil': ['巴西', '北里奥格兰德州', '纳塔耳'],
        'nri': ['巴西', '里约热内卢州', '尼泰罗伊'],
        'ntl': ['巴西', '北里奥格兰德州', '纳塔耳'],
        'oco': ['巴西', '圣保罗州', '奥萨斯库'],
        'pae': ['巴西', '南里奥格兰德州', '阿雷格里港'],
        'pmj': ['巴西', '托坎廷斯州', '帕尔马斯'],
        'pro': ['巴西', '圣保罗州', '里贝朗普雷图'],
        'pta': ['巴西', '伯南布哥州', '彼得罗利纳'],
        'pts': ['巴西', '里约热内卢州', '彼得罗波利斯'],
        'pvo': ['巴西', '朗多尼亚州', '波多韦柳'],
        'rbo': ['巴西', '阿克雷州', '里奥布朗库'],
        'rce': ['巴西', '伯南布哥州', '累西腓'],
        'rjo': ['巴西', '里约热内卢州', '里约热内卢'],
        'rpo': ['巴西', '圣保罗州', '里贝朗普雷图'],
        'sbo': ['巴西', '圣保罗州', '圣贝尔纳多－杜坎普'],
        'sdr': ['巴西', '巴伊亚州', '萨尔瓦多'],
        'sjc': ['巴西', '圣保罗州', '圣若泽－杜斯坎普斯'],
        'sls': ['巴西', '马拉尼昂州', '圣路易斯'],
        'sne': ['巴西', '圣保罗州', '圣安德烈'],
        'soc': ['巴西', '圣保罗州', '索罗卡巴'],
        'spo': ['巴西', '圣保罗州', '圣保罗'],
        'spo-mb': ['巴西', '圣保罗州', '圣保罗'],
        'sts': ['巴西', '圣保罗州', '桑托斯'],
        'tsa': ['巴西', '皮奥伊州', '特雷西纳'],
        'tte': ['巴西', '圣保罗州', '圣若泽－杜斯坎普斯'],
        'ula': ['巴西', '米纳斯吉拉斯州', '乌贝兰迪亚'],
        'vrd': ['巴西', '里约热内卢州', '沃尔塔雷东达'],
        'vta': ['巴西', '圣埃斯皮里图州', '维多利亚'],
        'atl': ['美国', '乔治亚州', '亚特兰大'],
        'mia': ['美国', '佛罗里达州', '迈阿密'],
        'nyk': ['美国', '纽约州', '纽约'],
    }
    for k, v in key.items():
        if f'.{k}' in host:
            return v
    return []


def format_c(ip):
    return '.'.join([f'{int(num):0>3d}' for num in ip.split('.')])


def get_c():
    with open('host.txt', 'r', encoding='utf-8') as fr:
        d_line = fr.readline()
        d_line_list = d_line.split(',')
        c = d_line_list[0].split('.')[:3]
        c.append('0')
        c = format_c('.'.join(c))
        return c


def get_host_parse_list():
    host_parse_list1 = list()
    with open('host.txt', 'r', encoding='utf-8') as fr:
        for d in fr:
            d_list = d.split(',')
            host_parse = parse(d_list[1])
            host_parse_list1.append([format_c(d_list[0]), host_parse])
    return host_parse_list1


def save_result_list(result_list):
    with open('text_c.txt', 'w', encoding='utf-8') as fw:
        fw.writelines(result_list)


def gen_template(ip, country, isp, isp_col, last_col):
    template_list = list()
    for i in range(256):
        current_ip = '.'.join(ip.split('.')[:3]) + f'.{i:0>3d}'
        if isp_col == '5':
            template_list.append('\t'.join([current_ip, current_ip, country, country, '*', '*', isp, '*', last_col]))
        elif isp_col == '4':
            template_list.append('\t'.join([current_ip, current_ip, country, country, '*', isp, '*', '*', last_col]))
    return template_list


if __name__ == '__main__': # 只能提取一个C
    COUNTRY = input('country:').strip()
    ISP = input('isp:').strip()
    ISP_COL = input('isp_col(pleas input "4" or "5"):').strip()
    while ISP_COL != '4' and ISP_COL != '5':
        ISP_COL = input('isp_col(pleas input "4" or "5"):').strip()
    LAST_COL = input('last_col:').strip() + '\n'

    c_ip = get_c()
    host_parse_list = get_host_parse_list()
    temp = gen_template(c_ip, COUNTRY, ISP, ISP_COL, LAST_COL)

    RESULT = list()

    for t in temp:  # '200.244.041.000	200.244.041.000	1	1	*	*	1	*	1
        t_list = t.split('\t')
        for h in host_parse_list:  # ['200.244.041.001', ['巴西', '圣保罗州', '圣保罗']]
            if t_list[0] == h[0]:
                for index, v in enumerate(h[1]):
                    t_list[2 + index] = v
                del (host_parse_list[0])
                RESULT.append('\t'.join(t_list))
                break
        else:
            RESULT.append(t)
    save_result_list(RESULT)
