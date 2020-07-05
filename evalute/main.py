import numpy as np

import sys
import pymysql


sys.path.append(r'./')
import getData
import createTimetable
import evalute
import putData
import dicfetchall

if __name__ == '__main__':
    db = pymysql.connect("localhost","root","zhangyu520","_timetabledb")
    cursor = db.cursor()
    sql='select * from wk'
    cursor.execute(sql)
    wkid_wk = dicfetchall.dictfetchall(cursor)
    for i in wkid_wk:
        print(i)
        sql='select * from pro_tclass'
        cursor.execute(sql)
        pro_tclass = dicfetchall.dictfetchall(cursor)
        for index in pro_tclass:
            print(index)
            wkid = i['wkid']
            wk = i['wk']
            pro = index['pro']
            tclass = index['tclass']
            data =getData.get_data(wk,pro,tclass) 
            timetable,d= createTimetable.cre_timetable(data)

            print(timetable)
            print(d)
   
            time = np.empty([6, 5], dtype=int)
            time = [
                [1, 2, 3, 4, 5],
                [1, 2, 3, 4, 5],
                [1, 2, 3, 4, 5],
                [1, 2, 3, 4, 5],
                [1, 2, 3, 4, 5],
                [1, 2, 3, 4, 5],
            ]  # 对应课程的日期

            CouScore = evalute.get_CouScore(timetable,time)
            print(CouScore)
            TableScore = evalute.get_TableScore(timetable)
            print(TableScore)
            putData.putCouScore(wkid,wk,pro,tclass,d,CouScore)
            putData.putTableScore(wkid,wk,pro,tclass,TableScore)