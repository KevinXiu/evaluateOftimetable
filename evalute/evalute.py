import numpy as np


def single_evalution(day_list):
    day_list.sort()
    s = day_list.__len__()
    score = 0
    if s == 2:    # 四学时
        d = day_list[1] - day_list[0]
        score = abs(d-3)
    elif s == 3:   # 周学时六学时，默认分三次上课
        d1 = abs(day_list[2] - day_list[1])
        d2 = abs(day_list[1] - day_list[0])
        score = (abs(d1-2)+abs(d2-2))/2
    elif s == 4:   # 八学时,默认分两次上课
        d = day_list[3] - day_list[0]
        score = abs(d-3)
    elif s == 1:   # 二学时
        score = 0
    if s==1:
        score = 100
    if s==2 or s==4:
        score = 100*(3-score)/3
    if s==3:
        score = 100*(2-score)/2
    return round(score,2)


def get_CouScore(schedule, time):
    data = schedule.flatten()
    course, count = np.unique(data, return_counts=True)  # 统计课程数及对应课程出现次数
   # print(course,count)
    arr = dict()
    for index, value in enumerate(count):
        if course[index] == 0:
            s1 = 0
        else:
            list = []
            for i, i_v in enumerate(schedule):
                for j, j_v in enumerate(i_v):
                    if j_v == course[index] and j_v != 0:
                        list.append(time[i][j])
            s1 = single_evalution(list)
            arr[index]=s1
    # print(arr)
    return arr


def get_TableScore(timetable):
    counts =[]
    for index in range(5):
        mylist = [x[index] for x in timetable]
        count = 0
        for i in mylist:
            if i != 0:
                count += 1
        counts.append(count)
    counts_var = np.var(counts)
    return round(100-counts_var,2)