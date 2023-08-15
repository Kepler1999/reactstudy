# use user and order api quiet
# do not request to many data one time, less than 100 is better

import requests as q
from tqdm import tqdm
import json

# region api url

user_api = "https://paike-support-be-wan.yunxiao.com/v1/paikeUser/userInfo?start=0&limit=10"

# permissions":["0"] : VIP
# permissionStatus":1 首次充值
# permissionStatus":2 续费用户
# tranRecord:1 订单数量

order_api = "https://paike-support-be-wan.yunxiao.com/v1/order/list/?status=done&start=0&limit=10"

# build fake request 
cookie = "paike-support-be=eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJsb2dpbk5hbWUiOiJ3YW5nZGkiLCJleHAiOjE2OTQzMzYyMTA2OTAsImlhdCI6MTY5MTc0NDIxMH0.GsACE4YQfXgFIRSoNzYZIHrYoF44OrMqd8AsOXuTVnM7NOq7wTZBKIkeKtlDVhyPUCPQMg3_qxYmcP7Q_FLdPg"

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
    "Cookie": cookie,
}

def get_user(start: int=0,limit:int =1) ->dict:
    url = "https://paike-support-be-wan.yunxiao.com/v1/paikeUser/userInfo?start={start}&limit={limit}".format(start=start,limit=limit)
    ret = q.get(url=url,headers=headers)
    
    return ret.json()
    
def get_user_amout() ->int:
    ret = get_user()
    amount = ret['data']['count']
    return amount

def get_user_byID(id:str) -> dict:
    url = f"https://paike-support-be-wan.yunxiao.com/v1/paikeUser/userInfobyId?userId={id}"
    ret = q.get(url=url,headers=headers)
    
    return ret.json()
    
# print(get_user_amout())    
    
def get_order(start: int=0,limit:int =1)->dict:
    url = "https://paike-support-be-wan.yunxiao.com/v1/order/list/?start={start}&limit={limit}".format(start=start,limit=limit)
    ret = q.get(url=url,headers=headers)
    
    return ret.json()

def get_order_amout() ->int:
    ret = get_order()
    amount = ret['data']['count']    
    return amount

# print(get_order_amout())

# def test():
#     import requests as r
#     ret = r.get(user_api,headers=headers)
#     print(ret.json())
# test success on 15 Aug

# endregion api url

# region model
from pony.orm import *

db = Database()
db.bind(provider='sqlite', filename='pk2.sqlite', create_db=True)
# db.bind(provider='postgres', user='', password='', host='', database='')

class School(db.Entity):
    id = PrimaryKey(str)
    name = Optional(str)  # 学校名称
    type = Optional(int)  # 学校类型
    area = Optional(str)  # 所在地区
    is_test = Required(bool,default=False)
    users = Set('User')


class User(db.Entity):
    id = PrimaryKey(int, auto=True)
    user_id = Optional(str)  # 排课系统用户id
    login_name = Optional(str)  # 登录用户名称
    phone = Optional(str)  # 电话号码
    email = Optional(str)  # 电子邮箱
    qq = Optional(str)  # qq号码
    status = Optional(str)  # 状态
    create_at = Optional(str)  # 创建时间
    last_active_at = Optional(str)  # 最后活跃时间
    school = Optional(School)
    orders = Set('Order')


class Order(db.Entity):
    id = PrimaryKey(str)
    spu = Optional(str)  # 商品SPU id
    sku = Optional(str)  # 商品SKU id
    amount = Optional(int)  # 订单金额
    status = Optional(str)  # 订单状态
    create_at = Optional(str)  # 订单创建时间
    pay_at = Optional(str)  # 支付时间
    close_at = Optional(str)  # 订单关闭时间，仅未支付订单存在值
    pay_channel = Optional(str)  # 支付方式
    serial_no = Optional(str)  # 交易单号
    user = Required(User)

# endregion model


# region sync data 

import time

@db_session
def sync_user_data():
    # get user amount and making group
    amount = get_user_amout()
    
    start = 0
    offset = 100
    
    data = []
    while True:
        if start >= amount:
            break
        
        time.sleep(1)        
        limit = offset if start+offset < amount else amount-start       

        print(f"{time.time()}::get user data from {start} to {start+limit} ")
        # handle        
        user_data = get_user(start=start,limit=limit)
        user_data = user_data['data']['list']
        
        # school data handle
        for usr in tqdm(user_data):
            # print(f"::{usr}")
            if usr['schoolId'] is None:
                data.append(usr)
                continue
                
            school = School.get(id=usr['schoolId'])
            if school is None:
                school = School(id=usr['schoolId'])
                school.name = usr['schoolName']
                school.type = usr['schoolType']
                school.area = usr['area']
                
                
        # user data handle
            user = User.get(login_name=usr['loginName'])
            if user is None:
                user = User()
                user.login_name=usr['loginName']
                user.phone = usr['phone'] if usr['phone'] is not None else ""
                user.email = usr['email'] if usr['email'] is not None else ""
                user.qq = usr['QQNumber'] if usr['QQNumber'] is not None else ""
                user.status = str(usr['status']) if usr['status'] is not None else ""
                user.create_at = str(usr['createdTime']) if usr['createdTime'] is not None else ""
                user.last_active_at = str(usr['lastUpdatedTime']) if usr['lastUpdatedTime'] is not None else ""
                
                user.school = school
            else:
                if str(usr['lastUpdatedTime']) not in user.last_active_at:
                    user.last_active_at = user.last_active_at + ";" + str(usr['lastUpdatedTime'])
            
            commit() 
                
        
        # end handle
        
        start = start + limit
    
    for d in data:
        with open('./emptyidschool.txt','a+',encoding='utf-8') as f:
            f.write(json.dumps(d))
    
# sync user data donot contains user id
# need handle it addtionally
import pandas as pd
@db_session
def add_user_id():

    # path = r"C:\Users\liang\Desktop\Repo\reactstudy\a.xlsx"
    
    path2 = r"C:\Users\liang\Desktop\Repo\reactstudy\userld.xlsx"
    
    df = pd.read_excel(path2)
    
    user = select(u for u in User if u.user_id=="")
    i = 0
    for u in tqdm(user[:]):
        # t = df[((str(df['LoginName']).strip())==u.login_name)]
        t = df[(df['LoginName']==u.login_name)]
        # print(t)
        user_id = t['Id'].values
        # print(user_id)
        if len(user_id)>0:
            u.user_id = str(user_id[0])
            i+=1
    print(i)

@db_session
def get_user_and_school_info():
    pass 
            
@db_session
def sync_order_data():
    # get user amount and making group
    amount = get_order_amout()
    
    start = 0
    offset = 100
    data = []
    
    while True:
        if start >= amount:
            break
        
        time.sleep(1)        
        limit = offset if start+offset < amount else amount-start
        
        print(f"{time.time()}::get order data from {start} to {start+limit} ")
        # handle        
        order_data = get_order(start=start,limit=limit)
        order_data = order_data['data']['list']      

        # order data handle
        # empty data
        
        for o in tqdm(order_data):  
            # print(f"::{o}")          
            order = Order.get(id=str(o['id']))
            if order is None:
                user = User.get(user_id=o['userId'])
                
                if user is None:
                    data.append(o)
                    continue
                # print(o['userId'],user)
                # order.user = user
                
                order = Order(id=str(o['id']),user=user)
                order.spu = o['spuId']
                order.sku = o['skuId']
                order.amount = o['amount']
                
                order.status = o['status']
                order.create_at = str(o['createdTime'])
                order.pay_at = str(o['notifyTime']) if o['notifyTime'] is not None else ""
                order.close_at = str(o['closeTime']) if o['closeTime'] is not None else ""
                
                order.pay_channel = o['payThrough']
                order.serial_no = o['tradeNo']
                


        commit()        
        start = start + limit
        
    for d in data:
        with open('./nouserorder.txt','a+',encoding='utf-8') as f:
            f.write(json.dumps(d))


# endregion sync data
# @db_session
# def needhelp():
#     user = select(u.login_name for u in User if u.user_id.startswith(" "))
#     for x in user[:]:
#         print(x)

if __name__ == "__main__":
    db.generate_mapping(create_tables=True)
    print(get_user_amout())
    # sync_user_data()
    # add_user_id()
    print(get_order_amout())
    # sync_order_data()
    # needhelp()