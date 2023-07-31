import secrets
import time


def get_id():
    return str(secrets.token_hex(16))


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


def get_national_list():
    s = """
    汉族、蒙古族、回族、藏族、维吾尔族、苗族、彝族、壮族、布依族、朝鲜族、满族、侗族、瑶族、白族、土家族、哈尼族、哈萨克族、傣族、黎族、僳僳族、佤族、畲族、高山族、拉祜族、水族、东乡族、纳西族、景颇族、柯尔克孜族、土族、达斡尔族、仫佬族、羌族、布朗族、撒拉族、毛南族、仡佬族、锡伯族、阿昌族、普米族、塔吉克族、怒族、乌孜别克族、俄罗斯族、鄂温克族、德昂族、保安族、裕固族、京族、塔塔尔族、独龙族、鄂伦春族、赫哲族、门巴族、珞巴族、基诺族
    """
    ss = str(s).split("、")
    return ss


def get_issue_code(platform: int = 1):
    import random
    prefix = None
    code = str(random.randint(1000, 10000))

    if platform == 1:  # 云平台
        prefix = "IDSP"
        return prefix + "-" + code
    elif platform == 2:  # 排课
        prefix = "PK"
        return prefix + "-" + code
