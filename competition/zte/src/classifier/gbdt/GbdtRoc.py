# coding=utf-8

import matplotlib.pyplot as plt

threshold = 0.0

f = open('E:/soft/Project/zte/ztedata/zte_face_test/test1/zte_output.txt', 'r')
read = f.readlines()
output_roc = open('E:/soft/Project/zte/ztedata/zte_face_test/test1/zte_roc.txt', 'w')

result = []
while (threshold < 1):
    fprNum = 0
    tprNum = 0
    for each in read:
        # str(i) + "," + str(predicty[i])+","+test_y[i]+"\n"
        eachs = each[:-1].split(",")
        if eachs[2] != '1' and float(eachs[1]) > threshold:
            fprNum += 1
        if eachs[2] == '1' and float(eachs[1]) > threshold:
            tprNum += 1
    # print threshold,fprNum,tprNum,float(fprNum)/3000,float(tprNum)/3000
    result.append([threshold, float(fprNum) / 3000, float(tprNum) / 3000])
    output_roc.write(str(threshold) + " " + str(float(fprNum) / 3000) + " " + str(float(tprNum) / 3000) + "\n")
    threshold += .01
tpr = [x[2] for x in result]
fpr = [x[1] for x in result]

# plt.plot(fpr,tpr,'b*')
plt.plot(fpr, tpr, 'r')
plt.xlabel("false positive rate")
plt.ylabel("true positive rate")
plt.title("ROC")
plt.legend()
plt.show()

output_roc.close()
f.close()
