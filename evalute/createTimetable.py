import numpy as np


def cre_timetable(data):
    count = 1
    timetable = np.zeros([6,5])
   # print(timetable)
    d = dict()
    for index in data:
        d[index.get('kcid')]=count
        # list1.append(d)
        str = index.get('time')
        sk_sj = str.split(',')
       # print(sk_sj)
        for s in sk_sj:
            times = s.split('.')
           # print(times)
            i = int(times[0])
            j = int (times[1])
            #print(i,j)
            timetable[j-1][i-1] = count
        count += 1
    return timetable,d