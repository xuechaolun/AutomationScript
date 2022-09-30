import time

start = time.time()

path4 = "C:/TianTexin/framework/library/ip/mydata.edit.txt"
path6 = "C:/TianTexin/framework/library/ip/mydata6.txt"

four_dict = dict()
five_dict = dict()

four_set = set()
five_set = set()


def add_two_dimensional_dictionary(old_dict, key_a, key_b, value):
    if key_a in old_dict:
        old_dict[key_a].update({key_b: value})
    else:
        old_dict.update({key_a: {key_b: value}})


with open(path4, 'r', encoding='utf-8') as fr:
    for d in fr:
        d_list = d.split('\t')
        if len(d_list) != 9:
            continue
        if d_list[5] != '*':
            four_set.add(d_list[5])
            # four_dict[d_list[5]] = 0
            add_two_dimensional_dictionary(four_dict, d_list[5], d_list[2], 0)
        if d_list[6] != '*':
            five_set.add(d_list[6])
            # five_dict[d_list[6]] = 0
            add_two_dimensional_dictionary(five_dict, d_list[6], d_list[2], 0)

with open(path6, 'r', encoding='utf-8') as fr:
    for d in fr:
        d_list = d.split('\t')
        if len(d_list) != 8:
            continue
        if d_list[4] != '*':
            four_set.add(d_list[4])
            # four_dict[d_list[4]] = 0
            add_two_dimensional_dictionary(four_dict, d_list[4], d_list[1], 0)
        if d_list[5] != '*':
            five_set.add(d_list[5])
            # five_dict[d_list[5]] = 0
            add_two_dimensional_dictionary(five_dict, d_list[5], d_list[1], 0)

same_domain = sorted(four_set & five_set)

# print(same_domain)

with open(path4, 'r', encoding='utf-8') as fr:
    for d in fr:
        d_list = d.split('\t')
        if len(d_list) != 9:
            continue
        if d_list[5] != '*':
            # four_dict[d_list[5]] += 1
            four_dict[d_list[5]][d_list[2]] += 1
        if d_list[6] != '*':
            # five_dict[d_list[6]] += 1
            five_dict[d_list[6]][d_list[2]] += 1

with open(path6, 'r', encoding='utf-8') as fr:
    for d in fr:
        d_list = d.split('\t')
        if len(d_list) != 8:
            continue
        if d_list[4] != '*':
            # four_dict[d_list[4]] += 1
            four_dict[d_list[4]][d_list[1]] += 1
        if d_list[5] != '*':
            # five_dict[d_list[5]] += 1
            five_dict[d_list[5]][d_list[1]] += 1


with open('result.txt', 'w', encoding='utf-8') as fw:
    for sd in same_domain:
        fw.write(sd)
        fw.write('\n\n第4列\n')
        for k, v in four_dict[sd].items():
            fw.write(str(k)+' '+str(v)+'\n')
        fw.write('\n第5列\n')
        for k, v in five_dict[sd].items():
            fw.write(str(k)+' '+str(v)+'\n')
        fw.write('\n--------------------\n')


end = time.time()

print(f'{len(same_domain)} 个 domain 有问题')
print(f'{end - start:.2f}s')
