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

# region statics


# endregion statics

if __name__ == "__main__":
    print(stamp2data1000(1692114980000))

