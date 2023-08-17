import time,datetime

# region func

def stamp2date(stamp:float = 100000000000) -> datetime.datetime:    
    dt = datetime.datetime.fromtimestamp(stamp)

    return dt

def stamp2data1000(stamp:str)-> datetime.datetime: 
    stamp = int(stamp)//1000
    dt = datetime.datetime.fromtimestamp(stamp)

    return dt

def date2stamp(da:datetime.datetime,thousand :int=1) -> str:
    if isinstance(da,datetime.datetime):
        stamp = da.timestamp()
        if thousand  == 1:
            return round(1000*stamp)
        return stamp
    

def get_localtime_std(localtime:datetime.datetime=datetime.datetime.now(), lite:bool=False):
    if lite is True:
        return localtime.strftime('%m/%d %H:%M:%S')
    return localtime.strftime('%Y/%m/%d %H:%M:%S')

# endregion func
import random
import string

def get_issue_code(platform:int=0) -> str:
    # 0 : IDSP
    # 1 : PK
    prefix = None
    match platform:
        case 0:
            prefix = "IDSP"
        case 1:
            prefix = "PK"
    
    return prefix +"-"+ "".join([str(x) for x in (random.sample(range(0,10),4))])
    


def func_exec_time(f):
    def inner(*arg, **kwarg):
        s_time = time.time()
        res = f(*arg, **kwarg)
        e_time = time.time()
        print(f'::Monitor:: "{f.__name__}" execute second(s)：{round(e_time - s_time, 4)}')
        return res

    return inner


def float2percentage(f: float, decimalplace=2) -> str:
    t = str(f * 100)
    if '.' not in t:
        return t + "%"

    t = t.rstrip('0')
    position = t.find('.')
    if len(t[position + 1:]) == 0:
        return t.rstrip('.') + "%"
    elif len(t[position + 1:]) <= decimalplace:
        return t.rstrip('0') + "%"
    else:
        return str(round(f * 100, decimalplace)) + "%"


def your_float(f: float, decimalplace=2) -> str:
    t = str(f)
    if '.' not in t:
        return t

    t = t.rstrip('0')
    position = t.find('.')
    if len(t[position + 1:]) == 0:
        return t.rstrip('.')
    elif len(t[position + 1:]) <= decimalplace:
        return t.rstrip('0')
    else:
        return str(round(f, decimalplace))


def get_rate_of_chage(a: float, b: float):
    if b == 0:
        return {"ret": "fail", "code": -1, 'msg': "对比值不接受0"}
    return float2percentage((a - b) / b)


def is_Chinese(word):
    for ch in word:
        if '\u4e00' <= ch <= '\u9fff':
            return True
    return False
# region statics


# endregion statics

if __name__ == "__main__":
    # print(stamp2data1000(1692114980000))
    print(get_localtime_std(datetime.datetime.now()))
    time.sleep(2)
    print(get_localtime_std(datetime.datetime.now()))

