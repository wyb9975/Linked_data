# 姓名：王宇彬 学号：3220190887
import pandas as pd
import numpy as np
# 处理Wine Reviews数据集，将两个表格连接在一起
io2 = "D:/dataMiner/winemag-data_first150k.csv"
data2 = pd.read_csv(io2)
io2 = "D:/dataMiner/winemag-data-130k-v2.csv"
data2_1 = pd.read_csv(io2)
data2 = data2.append(data2_1)

# 处理dataFrame，使得序号连续
data2 = data2.reset_index(drop = True)
data_filtrated2 = data2.copy()
# 标称属性
#category_col = ['country','province','region_1','region_2','taster_name','taster_twitter_handle','variety','winery']
category_col = ['country','taster_name','taster_twitter_handle','variety','winery']
#利用高频数值填充缺失值
for item in category_col:
    # 计算最高频率的值
    most_frequent_value = data_filtrated2[item].value_counts().idxmax()
    # 替换缺失值
    data_filtrated2[item].fillna(value = most_frequent_value, inplace = True)
    
# Apriori算法计算频繁项
import sys
def apriori(D, minSup):
    '''频繁项集用keys表示，
    key表示项集中的某一项，
    cutKeys表示经过剪枝步的某k项集。
    C表示某k项集的每一项在事务数据库D中的支持计数
    '''
    C1 = {}
    for T in D:
        for I in T:
            if I in C1:
                C1[I] += 1
            else:
                C1[I] = 1

    _keys1 = C1.keys()

    keys1 = []
    for i in _keys1:
        keys1.append([i])
    n = len(D)
    cutKeys1 = []
    for k in keys1[:]:
        if C1[k[0]]*1.0/n >= minSup:
            cutKeys1.append(k)
    cutKeys1.sort()
    keys = cutKeys1
    all_keys = []
    all_sups = []
    while keys != []:
        C = getC(D, keys)
        cutKeys,sups = getCutKeys(keys, C, minSup, len(D))
        for key in cutKeys:
            all_keys.append(key)
        for sup in sups:
            all_sups.append(sup)
        keys = aproiri_gen(cutKeys)
    return all_keys,all_sups

def getC(D, keys):
    '''对keys中的每一个key进行计数'''
    C = []
    for key in keys:
        c = 0
        for T in D:
            have = True
            for k in key:
                if k not in T:
                    have = False
            if have:
                c += 1
        C.append(c)
    print(C)
    return C

def getCutKeys(keys, C, minSup, length):
    '''剪枝步'''
    kk = []
    sups = []
    for i, key in enumerate(keys):
        if float(C[i]) / length >= minSup:
            #keys.remove(key)k
            kk.append(key)
            sups.append(float(C[i]) / length)
    #print(kk)
    return kk,sups



def keyInT(key, T):
    '''判断项key是否在数据库中某一元组T中'''
    for k in key:
        if k not in T:      # 只要有一个不匹配，就返回False
            return False
    return True


def aproiri_gen(keys1):
    '''连接步'''
    keys2 = []
    for k1 in keys1:
        for k2 in keys1:
            if k1 != k2:
                key = []
                for k in k1:
                    if k not in key:
                        key.append(k)
                for k in k2:
                    if k not in key:
                        key.append(k)
                key.sort()
                if key not in keys2:
                    keys2.append(key)

    return keys2
# 取数据值中包含标称数据的列
data_category = data_filtrated2[category_col]
# 将dataframe转化为数组形式
data_array=data_category.values
# 设置最低支持度为0.1，计算频繁项，并返回频繁项数组以及对应的支持度数组
fre,sups = apriori(data_array,0.1)

str = []
for i in range(len(fre)):
    temp = ''
    for item in fre[i]:
        temp = temp + item + ' '
    str.append(temp)

# 对于每个关联规则，计算提升度并展示
confis = []
for i in range(len(fre)):
    config = sups[i]
    for k in fre[i]:
        for j in range(len(fre)):
            if len(fre[j]) == 1 and fre[j][0] == k:
                config = config / sups[j]
    confis.append(config)
number = 2
ss = []
nums = []
for i in range(len(confis)):
    if len(fre[i]) == 1:
        continue
    if len(fre[i]) == number:
        nums.append(confis[i])
        ss.append(str[i])
    else:
        plt.figure(figsize=(20,5))
        plt.bar(ss, nums)
        plt.title('lift result')
        plt.show()
        ss = []
        nums = []
        nums.append(confis[i])
        ss.append(str[i])
        break

#对于每个关联规则，计算置信度并展示
for i in range(len(fre)):
    config = sups[i]
    c = []
    names = []
    if len(fre[i]) != 2:
        continue
    for k in fre[i]:
        for j in range(len(fre)):
            if len(fre[j]) == 1 and fre[j][0] == k:
                temp = config / sups[j]
                c.append(temp)
                names.append(k)
                break
    plt.bar(names, c)
    plt.title('confidence result')
    plt.show()
 
#对于每个关联规则，计算allconf指标并展示
nn = []
nums_2 = []
for i in range(len(fre)):
    if len(fre[i]) != 2:
        continue
    max = -1
    for j in range(len(fre)):
        if len(fre[j]) == 1 and confis[j] > max:
            max = confis[j]
    nn.append(str[i])
    nums_2.append(confis[i] / max)
plt.figure(figsize=(20,5))
plt.bar(nn, nums_2)
plt.title('allconf result')
plt.show()
