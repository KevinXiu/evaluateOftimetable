import pymysql

import sys
sys.path.append(r'./')
import dicfetchall


def putCouScore(wkid,wk,pro,tclass,d,CouScore):
    db = pymysql.connect("localhost","root","zhangyu520","_timetabledb")
    # 使用cursor()方法获取操作游标 
    cursor = db.cursor()
    for i in CouScore:

        kcid = list(d.keys())[list(d.values()).index(i)]

        cu = db.cursor()
        sql = "select kcmc from kc_info where  kcid = '{}'".format(kcid)
        cu.execute(sql)
        sou_dict =dicfetchall.dictfetchall(cu)
        sourse = sou_dict[0]['kcmc']
 # SQL 插入语句
        sql = "INSERT INTO test1(wkid, wk,pro, tclass, sourse, score) VALUES ({},'{}','{}','{}','{}',{})".format(wkid,wk,pro,tclass,sourse,CouScore[i])
        try:
   # 执行sql语句
            cursor.execute(sql)
   # 提交到数据库执行
            db.commit()
        except:
   # 如果发生错误则回滚
                db.rollback()
 
# 关闭数据库连接
    db.close()


def putTableScore(wkid,wk,pro,tclass,TableScore):
    db = pymysql.connect("localhost","root","zhangyu520","_timetabledb")
    # 使用cursor()方法获取操作游标 
    cursor = db.cursor()
    sql = "INSERT INTO test2(wkid,wk,pro, tclass, score) VALUES ({},'{}','{}','{}',{})".format(wkid,wk,pro,tclass,TableScore)
    try:
   # 执行sql语句
        cursor.execute(sql)
   # 提交到数据库执行
        db.commit()
    except:
   # 如果发生错误则回滚
        db.rollback()
 
# 关闭数据库连接
    db.close()