import streamlit as st
import pandas as pd
from pony.orm import *

from pk import db, School, User, Activity, Order, Collection, check_collection

from tools import date2stamp, get_rate_of_chage, float2percentage

from datetime import date, datetime, timedelta


stand_date = date.today() - timedelta(days=2)


# head

st.title("PK-app Data Tracking")
st.write(f"统计周期：2022-01-01~{stand_date}, 每日2:00am 更新数据")
st.write(f"1.当日，指{stand_date}，近15日、今年同期的截止日期均为此；")
st.write("2.由于原数据库用户活跃记录错误，{stand_date}之前的日活用户仅供参考.")
st.write("3.数据仅包含线上支付的订单、营收等数据，线下签订合同银行转账的记录无法纳入。")
st.write("")

# region date define

# today & lastyear_today
today = stand_date
today_s = date2stamp(datetime(today.year, today.month, today.day, 0, 0, 0))
today_e = date2stamp(datetime(today.year, today.month, today.day, 23, 59, 59))

last_year_today = today - timedelta(days=365)
last_year_today_s = date2stamp(
    datetime(last_year_today.year, last_year_today.month, last_year_today.day, 0, 0, 0)
)
last_year_today_e = date2stamp(
    datetime(
        last_year_today.year, last_year_today.month, last_year_today.day, 23, 59, 59
    )
)

# 15days
day_15 = today - timedelta(days=15)
day_15_s = date2stamp(datetime(day_15.year, day_15.month, day_15.day, 0, 0, 0))
day_15_e = today_e

last_year_day_15 = day_15 - timedelta(days=365)
last_year_day_15_s = date2stamp(
    datetime(
        last_year_day_15.year, last_year_day_15.month, last_year_day_15.day, 0, 0, 0
    )
)
last_year_day_15_e = last_year_today_e

# this year span
this_year_s = date2stamp(datetime(today.year, 1, 1, 0, 0, 0))
this_year_e = today_e

last_year_s = date2stamp(datetime(last_year_today.year, 1, 1, 0, 0, 0))
last_year_e = last_year_today_e

# last whole year
last_whole_year_s = last_year_s
last_whole_year_e = date2stamp(datetime(last_year_today.year, 12, 31, 23, 59, 59))

# endregion


@st.cache_data
@db_session
def get_specified_start_end_data():
    data = {}

    # today & last year today
    d_today = check_collection(today_s, today_e)
    d_last_year_today = check_collection(last_year_today_s, last_year_today_e)

    data["today"] = d_today
    data["last_year_today"] = d_last_year_today

    # 15days
    d_15_day = check_collection(day_15_s, day_15_e)
    d_last_year_15_day = check_collection(last_year_day_15_s, last_year_day_15_e)

    data["15day"] = d_15_day
    data["last_year_15day"] = d_last_year_15_day

    # this year span
    d_this_year = check_collection(this_year_s, this_year_e)
    d_last_year = check_collection(last_year_s, last_year_e)

    data["thisyear"] = d_this_year
    data["lastyear"] = d_last_year

    # last whole year
    d_last_whole_year = check_collection(last_whole_year_s, last_whole_year_e)

    data["lastwholeyear"] = d_last_whole_year

    return data


# 单项

st.subheader("总览")

# region
compared_data = get_specified_start_end_data()

# income data
income_today = compared_data["today"]["income"]
income_15_days = compared_data["15day"]["income"]
income_this_year = compared_data["thisyear"]["income"]

income_today_ly = compared_data["last_year_today"]["income"]
income_15_days_ly = compared_data["last_year_15day"]["income"]
income_last_year = compared_data["lastyear"]["income"]
income_last_whole_year = compared_data["lastwholeyear"]["income"]

# active users
dau_today = compared_data["today"]["dau"]
dau_15_days = compared_data["15day"]["dau"]
dau_this_year = compared_data["thisyear"]["dau"]

dau_today_ly = compared_data["last_year_today"]["dau"]
dau_15_days_ly = compared_data["last_year_15day"]["dau"]
dau_last_year = compared_data["lastyear"]["dau"]
dau_last_whole_year = compared_data["lastwholeyear"]["dau"]

# new users
register_today = compared_data["today"]["register"]
register_15_days = compared_data["15day"]["register"]
register_this_year = compared_data["thisyear"]["register"]

register_today_ly = compared_data["last_year_today"]["register"]
register_15_days_ly = compared_data["last_year_15day"]["register"]
register_last_year = compared_data["lastyear"]["register"]
register_last_whole_year = compared_data["lastwholeyear"]["register"]

# order user, pay or not payed both in
order_user_today = compared_data["today"]["order_from_user"]
order_user_today_ly = compared_data["last_year_today"]["order_from_user"]

order_user_15day = compared_data["thisyear"]["order_from_user"]
order_user_15day_ly = compared_data["lastyear"]["order_from_user"]

# endregion
st.write("> 营收")


col1, col2, col3, col4 = st.columns(4)
col1.metric(
    "当日", f"{income_today}", f"{get_rate_of_chage(income_today,income_today_ly)}"
)
col2.metric(
    "近15天",
    f"{income_15_days}",
    f"{get_rate_of_chage(income_15_days,income_15_days_ly)}",
)
col3.metric(
    "当年(对比去年同期)",
    f"{income_this_year}",
    f"{get_rate_of_chage(income_this_year,income_last_year)}",
)
col4.metric("当年完成去年全年", f"{float2percentage(income_this_year/income_last_whole_year)}")

# st.subheader("用户活跃")
# st.text("由于活跃用户数据")
#####################################################
st.divider()
st.write("> 新注册用户")


a1, a2, a3 = st.columns(3)
a1.metric(
    "当日", f"{register_today}", f"{get_rate_of_chage(register_today,register_today_ly)}"
)
a2.metric(
    "近15天",
    f"{register_15_days}",
    f"{get_rate_of_chage(register_15_days,register_15_days_ly)}",
)
a3.metric(
    "当年(对比去年同期)",
    f"{register_this_year}",
    f"{get_rate_of_chage(register_this_year,register_last_year)}",
)


@st.cache_data
@db_session
def get_order_pay_school_data():
    data = {}
    # 当年复购绿
    last_year_paid_user = distinct(
        o.user
        for o in Order
        if o.status == "done"
        and o.create_at > str(last_year_s)
        and o.create_at < str(last_year_e)
    )
    
    this_year_paid_user = distinct(
        o.user
        for o in Order
        if o.status == "done"
        and o.create_at > str(this_year_s)
        and o.create_at < str(this_year_e)
    )
    
    last_paid_and_this_year_paid_user = [u for u in last_year_paid_user[:] if u in this_year_paid_user[:] ]
    
    # r_u = []
    # for i in u[:]:
    #     success_orders = select(a for a in Order if a.user == i and a.status == "done").count()
    #     if success_orders >= 2:
    #         r_u.append(i)
    # if len(u[:])<=0:
    #     repeat_pay_ratio_this_year = "0.0%"
    # else:
    repeat_pay_ratio_this_year = float2percentage(len(last_paid_and_this_year_paid_user)/len(last_year_paid_user[:]))
    
    data['repeat_pay_ratio_this_year']=repeat_pay_ratio_this_year
        
    # 总体转化率
    user_amount = select(u for u in User).count()
    pay_user_amount = select(o.user for o in Order if o.status == "done").count()
    
    trans_ratio = float2percentage(pay_user_amount/user_amount)
    
    data['trans_ratio'] =trans_ratio

    # 学校数据
    u = select(a for a in School if a.is_test==False).count()
    school_has_user = u
    
    data['school_has_user']=school_has_user
    
    u = select(a for a in School if a.is_test==False and "done" in a.users.orders.status).count()       
    school_has_paid = u
    
    data['school_has_paid'] = school_has_paid
    
    
    # u = select(a for a in School if a.is_test==False and any(a.user.orders.status) == "done").count()  
    # school_is_vip = 0
    
    data['school_trans_rate'] =float2percentage(school_has_paid/school_has_user)
    
    
    
    return data

###############################
st.divider()
st.write("> 下单、转化和复购。 说明：下单人数包括下单未支付用户")


o_t_s_data = get_order_pay_school_data()

p1, p2, p3, p4 = st.columns(4)
p1.metric(
    "当日下单人数",
    f"{order_user_today}",
    f"{get_rate_of_chage(order_user_today,order_user_today_ly)}",
)
p2.metric(
    "15日下单人数",
    f"{order_user_15day}",
    f"{get_rate_of_chage(order_user_15day,order_user_15day_ly)}",
)
p3.metric(
    "当年复购率",f"{o_t_s_data['repeat_pay_ratio_this_year']}"
)
p4.metric(
    "总体转化率",f"{o_t_s_data['trans_ratio']}"
)

###############################
st.divider()
st.write("> 学校覆盖情况")


s1,s2,s3 = st.columns(3)
s1.metric(
    "触达学校数量",
    f"{o_t_s_data['school_has_user']}",

)

s2.metric(
    "付费学校数量",
    f"{o_t_s_data['school_has_paid']}",

)
s3.metric(
    "学校转化率",
    f"{o_t_s_data['school_trans_rate']}",

)


# 用户预警
st.divider()
st.subheader("预警提示")
st.text("TBC")

# 综合
st.divider()
st.subheader("分项详情")


@st.cache_data
@db_session
def get_data():
    # db.generate_mapping()
    data = select(a for a in Collection).order_by(Collection.date)

    index = [a.date for a in data]
    # index = index[:]

    register = [a.register for a in data]
    df_register = pd.DataFrame(columns=["注册用户数"], index=index, data=register[:])

    dau = [a.dau for a in data]
    df_dau = pd.DataFrame(columns=["活跃用户数量"], index=index, data=dau[:])

    data_order = []
    orders_place = [a.order_place for a in data]
    data_order.append(orders_place[:])
    orders_user = [a.order_from_user for a in data]
    data_order.append(orders_user[:])
    orders_success = [a.order_success for a in data]
    data_order.append(orders_success[:])

    df_order = pd.DataFrame(
        columns=[
            "下单量",
        ],
        data=data_order[0],
    )
    df_order = pd.concat(
        [
            df_order,
            pd.DataFrame(
                columns=[
                    "下单人数",
                ],
                data=data_order[1],
            ),
        ],
        axis=1,
    )
    df_order = pd.concat(
        [
            df_order,
            pd.DataFrame(
                columns=[
                    "成交订单数量",
                ],
                data=data_order[2],
            ),
        ],
        axis=1,
    )
    df_order.index = index

    income = [a.income for a in data]
    df_income = pd.DataFrame(columns=["营收"], index=index, data=income[:])

    return {
        "df_register": df_register,
        "df_dau": df_dau,
        "df_order": df_order,
        "df_income": df_income,
    }


a = get_data()


st.write("> 注册用户")
st.line_chart(a["df_register"])


st.write("> 活跃用户")
st.line_chart(a["df_dau"])


st.write("> 订单量")
st.line_chart(a["df_order"])


st.write("> 营收")
st.bar_chart(a["df_income"])
