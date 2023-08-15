# import random 
# from tqdm import tqdm
# from collections import Counter

# dd = []
# for i in tqdm(range(0, 100000)):
#     a = random.randint(1, 33)
#     b = random.randint(1, 33)
#     c = random.randint(1, 33)
#     d = random.randint(1, 33)
#     e = random.randint(1, 33)
#     f = random.randint(1, 13)
#     g = random.randint(1, 13)
    
#     dd.append(a)
#     dd.append(b)
#     dd.append(c)
#     dd.append(d)
#     dd.append(e)
#     dd.append(f)
#     dd.append(g)

# print(random.sample(dd,7))

import requests as re

url = 'http://127.0.0.1:10001/geography/country/'
data = {'name_chs':'中国','name_eng':"China"}

p = re.post(url, params=data)
print(p.text)