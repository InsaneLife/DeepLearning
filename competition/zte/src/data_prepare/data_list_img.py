# -*- coding:utf8 -*-

f = open('./datalist.txt', 'rb')
f_people_1 = open('./people_1_ZTE', 'wb')
f_people_2 = open('./people_2_ZTE', 'wb')
f_label = open('./label_ZTE', 'wb')

lines = f.readlines()
for line in lines:
    linestr = line.split(':')
    f_people_1.write(
        linestr[0].replace(
            'pictures',
            '/home/work/ZTE_croped_images/person/' + linestr[0][9:16]) +
        ',' +
        linestr[2].replace(
            '\r',
            ''))
    f_people_2.write(
        linestr[1].replace(
            'pictures',
            '/home/work/ZTE_croped_images/person/' + linestr[1][9:16]) +
        ',' +
        linestr[2].replace(
            '\r',
            ''))
    f_label.write(linestr[2].replace('\r', ''))
