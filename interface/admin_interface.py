from db import db_handler
from lib import common

admin_logger = common.get_logger('admin')

# 管理员修改额度接口
def admin_modify_balance_interface(change_user, money):
    # 获取用户字典
    user_dic = db_handler.select(change_user)
    # 用户不存在，提示重新输入
    if user_dic:
        # 用户存在,执行修改操作
        user_dic['balance'] = money
        db_handler.save(user_dic)
        msg = f'管理员修改用户：[{change_user}] 余额成功，当前余额为 [{money}] '
        admin_logger.info(msg)
        return True, msg
    else:
        msg = '用户不存在，请重新输入'
        admin_logger.warn(msg)
        return False, msg


# 冻结账户接口
def lock_user_interface(username):
    user_dic = db_handler.select(username)
    if user_dic:
        # 将locked的默认值改为True
        user_dic['locked'] = True
        db_handler.save(user_dic)
        msg = f'管理员冻结用户：[{username}] 成功！'
        admin_logger.info(msg)
        return True, msg
    else:
        msg = '冻结用户不存在！'
        admin_logger.warn(msg)
        return False, msg