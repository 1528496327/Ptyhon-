"""
数据处理层
    - 专门用于处理数据的
"""


import json
import os
from conf import settings

# 查看数据
def select(username):
    # 1）接收接口层传过来的username用户名，拼接用户json文件路径
    user_path = os.path.join(
        settings.USER_DATA_PATH, f'{username}.json'
    )
    # 2）校验用户json文件是否存在
    if os.path.exists(user_path):
        # 3）打开数据，并返回给接口层
        with open(user_path, 'r', encoding='utf-8') as f:
            user_dic = json.load(f)
            return user_dic

# 保存数据
def save(user_dic):
    # 1) 拼接用户的数据字典
    username = user_dic.get('username')
    user_path = os.path.join(
        settings.USER_DATA_PATH, f'{username}.json'
    )
    # 2) 保存用户的数据
    with open(user_path, 'w', encoding='utf-8') as f:
        json.dump(user_dic, f, ensure_ascii=False)  # ensure_ascii=False让文件中的中文显示