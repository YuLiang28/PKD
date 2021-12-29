import string
import random

# 生成激活码
def generate_keys(total):
    keySet = set() # 设置一个集合变量，集合内不重复，可以过滤重复项
    while len(keySet) != total: # 循环执行，keySet 长度等于用户输入生成数量时结束
        keyStr = '' # 激活码临时存放变量
        for i in range(16): # 循环生成每一位激活码
            point = random.randint(0, 4) # 数字概率 1/5  4  小写字母为 2/5 [0,1]  大写字母概率 2/5 [2,3]
            if point == 0 or point == 1:
                lowKey = str(random.sample(string.ascii_lowercase, 1)) # 从指定的序列中,随机的截取指定长度的片断
                keyStr = keyStr+lowKey
            elif point == 2 or point == 3:
                upKey = str(random.sample(string.ascii_uppercase, 1))
                keyStr = keyStr + upKey
            elif point == 4:
                dKey = str(random.sample(string.digits, 1))
                keyStr = keyStr + dKey
            
            keyStr = keyStr.replace('[', '').replace(']', '') # 替换字符串中无效字符
            keyStr = keyStr.replace("'", '') # 替换字符串中无效字符

        keyStr = keyStr[0:4]+'-'+keyStr[5:9]+'-'+keyStr[8:12]+'-'+keyStr[12:] # 添加激活码连接符
        keySet.add(keyStr) # 添加激活码到集合中
    return keySet

if __name__ == '__main__':
    dset = generate_keys(100)
    for d in dset:
        print(d)
