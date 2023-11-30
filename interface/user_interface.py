"""
逻辑接口层
    用户接口
"""
from db import db_handler
from lib import common

user_logger = common.get_logger('user')

# 注册接口
def register_interface(username, password, balance=15000):
    # 2）查看用户是否存在
    # 2.1） 调用数据处理层 中的 select 函数，返回一个 用户字典 或 None
    user_dic = db_handler.select(username)
    # 若用户存在，则return，告诉用户重新输入
    if user_dic:
        return False, '用户名已存在！'  # 这边等同于return 了一个元组，元组里有两个值
    # 3）用户名不存在，保存用户数据
    # 密码加密
    password = common.get_pwd_md5(password)

    # 3.1）组织用户的数据的字典信息
    user_dic = {
        'username': username,
        'password': password,
        'balance': balance,
        'flow': [],  # 用于记录用户流水的列表
        'shop_car': {},  # 用于记录用户的购物车
        'locked': False  # 用于记录用户是否被冻结， False未冻结，True已冻结
    }

    # 3.2）保存数据
    db_handler.save(user_dic)
    msg = f'{username}注册成功！'
    # 记录日志
    user_logger.info(msg)
    return True, msg

# 登录接口
def login_interface(username, password):
    # 1）先查看当前用户数据是否存在
    user_dic = db_handler.select(username)
    # 2）判断用户是否存在



    if user_dic:
        # 给用户输入的密码做一次加密
        password = common.get_pwd_md5(password)
        # 3）校验密码是否一致
        if password == user_dic.get('password'):
            # 判断用户是否被锁定
            if user_dic.get('locked'):
                return False, '当前用户已被锁定'
            msg = f'用户: [{username}] 登录成功！'
            user_logger.info(msg)  # 记录日志
            return True, msg
        else:
            msg = '密码错误，请重新输入！'
            user_logger.warn(msg)
            return False, msg
    msg = f'[{username}] 用户不存在，请重新输入！'
    user_logger.info(msg)
    return False, msg

# 查看余额接口
def check_bal_interface(username):
    user_dic = db_handler.select(username)

    return user_dic.get('balance')