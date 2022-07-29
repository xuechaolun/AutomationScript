
def b(f, s):
    f_list = f.split('.')
    s_list = s.split('.')
    if (f_list[3] != '0' and f_list[3] != '000') or s_list[3] != '255':
        flag = 3
    else:
        flag = 2
    return True if f_list[:flag] == s_list[:flag] else False


def main():
    with open('text_c.txt', mode="r", encoding='utf-8') as fr:
        with open("result.txt", mode="w", encoding='utf-8') as fw:
            d1 = fr.readline()
            while d1:
                d2 = fr.readline()
                d1_list = d1.split('\t')
                d2_list = d2.split('\t')
                if d1_list[2:] == d2_list[2:] and b(d1_list[0], d2_list[1]):
                    d2_list[0] = d1_list[0]
                else:
                    fw.write(d1)
                d1 = '\t'.join(d2_list)


if __name__ == '__main__':
    main()
