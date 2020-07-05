import datetime
from django.shortcuts import render
from django.views import View
from django.http import JsonResponse, HttpResponseRedirect
from django.db import connection


# Create your views here.

def dictfetchall(cursor):
    """转换成字典格式"""
    desc = cursor.description
    return [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]


def index(r):
    return HttpResponseRedirect('static/index.html')


class GetDatas(View):
    """
    获取专业,周，班级
    """

    def get(self, r):
        cu = connection.cursor()
        cu.execute("select wk from kc_score group by wk")
        wk = dictfetchall(cu)
        #专业班级
        #cu.execute("select tclass from data group by tclass")
        cu.execute("select distinct pro ,tclass from kc_score ")
        ans = dictfetchall(cu)
        pro_class = []
        for i in ans:
            d = dict()
            d['pro_class'] = i['pro']+i['tclass']
            pro_class.append(d)
        # print((pro_class))
        # print(pro_class[0]['pro_class'][-2:])
        cu.execute("select pro from kc_score group by pro")
        pro = dictfetchall(cu)
        return JsonResponse({'code': 0, 'wk': wk, 'pro': pro, 'pro_class': pro_class})

class Tdb(View):
    """
    获取图一数据
    """

    def get(self, r):
        pro = r.GET.get('pro')
        cu = connection.cursor()
        # if not pro:
        #     sql = "select wk,tclass,sum(score)sc from data group by wk,tclass order by wkid;"
        # else:
        #     sql = "select wk,tclass,sum(score)sc from data where pro='{}'  group by wk,tclass order by wkid;".format(
        #         pro, )
        # if pro:
        #     sql = "select wk ,tclass ,score(sum) sc from data where  pro = '{}' order by wkid;".format(pro)
        # else:
        #     sql = "select wk ,tclass ,score from data where  pro = '{}'  order by wkid;".format("通信工程")

        if pro:
            sql = "select wk ,tclass ,score from kb_score where  pro = '{}'  group by wk,tclass order by wkid;".format(pro)
        else:
            sql = "select wk ,tclass ,score from kb_score where  pro = '{}' group by wk,tclass  order by wkid;".format("通信工程")


        cu.execute(sql)
        data = dictfetchall(cu)
        # print(data)
        source = []
        # 获取所有班级
        # cu.execute("select tclass from data group by tclass")
        if pro:
            sql = "select distinct tclass from kc_score where pro = '{}'".format(pro)
        else:
            sql = "select distinct tclass from kc_score where pro = '{}'".format("通信工程")
        cu.execute(sql)
        cl = dictfetchall(cu)
        # print(cl)
        dimensions = ['product']
        for c in cl:
            dimensions.append(c.get('tclass'))
        # print(dimensions)
        tmp = {}
        dataset = {}
        for i in data:

            if i.get('wk') not in tmp:
                tmp.update({i.get('wk'): [{i.get('tclass'): i.get('score')}]})
            else:
                tmp[i.get('wk')].append({i.get('tclass'): i.get('score')})
        # print(tmp)
        for k, v in tmp.items():
            t = {'product': k}
            for i in v:
                t.update(i)
                source.append(t)
        # print(source)
        dataset.update({'dimensions': dimensions, 'source': source})
        # print(dataset)
        return JsonResponse({'code': 0, 'dataset': dataset})


class T1db(View):
    """
    图2数据
    """

    def get(self, r):
        wk = r.GET.get('wk')
        # tclass = r.GET.get('tclass')
        pro_class = r.GET.get('pro_class')
        cu = connection.cursor()
        # sql = "select sourse, sum(score) sc from data where 1=1  "
        # if wk:
        #     sql += ' and wk="{}"'.format(wk)
        # if tclass:
        #     sql += ' and tclass="{}"'.format(tclass, )
        # sql += 'group by sourse'
        sql = "select sourse ,score from kc_score where "
        if wk:
            sql += 'wk="{}"'.format(wk)
        else:
            sql += 'wk="{}"'.format("第一周")
        if pro_class:
            pro = pro_class[0:-2]
            tclass = pro_class[-2:]
            sql +=' and pro = "{} " and tclass = "{}"'.format(pro, tclass)
        else:
            sql +=' and pro = "{} " and tclass = "{}"'.format('通信工程', '二班')
        cu.execute(sql)
        data = dictfetchall(cu)
        xdata = []
        sdata = []
        for i in data:
            xdata.append(i.get('sourse'))
            sdata.append(i.get('score'))

        return JsonResponse({'code': 0, 'xdata': xdata, 'sdata': sdata})
