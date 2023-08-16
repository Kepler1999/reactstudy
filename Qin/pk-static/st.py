import streamlit as st
import pandas as pd

from datetime import date,datetime,timedelta

from pk import db,Collection
from pony.orm import *


st.write("# PK-app Data Tracking")
st.write(f"*统计周期：2022-01-01~{date.today()-timedelta(days=2)}, 每日2:00am 更新数据*")
st.text("Notice:由于原数据库用户活跃记录错误，2023-08-14之前的日活用户仅供参考。")


@st.cache_data
@db_session
def get_data():    
    db.generate_mapping()    
    data = select(a for a in Collection).order_by(Collection.date)
   
    index = [a.date for a in data]
    # index = index[:]
    
    register = [a.register for a in data]    
    df_register = pd.DataFrame(columns=["注册用户数"],index=index,data=register[:])
    
    dau = [a.dau for a in data]
    df_dau = pd.DataFrame(columns=["活跃用户数量"],index=index,data=dau[:])
    
    data_order = []
    orders_place = [a.order_place for a in data]
    data_order.append(orders_place[:])   
    orders_user = [a.order_from_user for a in data]
    data_order.append(orders_user[:])
    orders_success = [a.order_success for a in data]
    data_order.append(orders_success[:])
    
    df_order = pd.DataFrame(columns=["下单量",],data=data_order[0])
    df_order = pd.concat([df_order,pd.DataFrame(columns=["下单人数",],data=data_order[1])],axis=1)
    df_order = pd.concat([df_order,pd.DataFrame(columns=["成交订单数量",],data=data_order[2])],axis=1)
    df_order.index = index
    
    income = [a.income for a in data]
    df_income = pd.DataFrame(columns=["营收"],index=index,data=income[:])
    
    return{
        "df_register":df_register,
        "df_dau":df_dau,
        "df_order":df_order,
        "df_income":df_income,
    }
    
a = get_data()

st.subheader("注册用户")
st.line_chart(a["df_register"])


st.subheader("活跃用户")
st.line_chart(a["df_dau"])

st.subheader("订单量")
st.line_chart(a["df_order"])

st.subheader("营收")
st.bar_chart(a["df_income"])
