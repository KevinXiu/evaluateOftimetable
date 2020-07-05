import pymysql
import sys
sys.path.append(r'./')
import dicfetchall



def get_data(wk,pro,tclass):
    db = pymysql.connect("localhost","root","zhangyu520","_timetabledb")
    cursor = db.cursor()
    sql = "select * from kc_time where wk='{}' and pro ='{}'and tclass = '{}' ".format(wk,pro,tclass)
    cursor.execute(sql)
    data = dicfetchall.dictfetchall(cursor)
    db.close()
    return data