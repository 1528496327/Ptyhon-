"""
银行相关业务的接口
"""
from db import db_handler
from lib import common
bank_logger = common.get_logger('bank')
# 提现接口
def withdraw_interface(username, money):
    # 1）先获取用户字典
    user_dic = db_handler.select(username)
    # 2）校验用户的钱是否足够
    balance = int(user_dic.get('balance'))
    money2 = int(money) * 1.05  # 手续费 5%
    if balance >= money2:
        # 2）修改数据字典的金额
        balance -= money2
        user_dic['balance'] = balance

        # 3）记录流水
        flow = f'用户 [{username}] 提现金额 [{money}] 成功，手续费为 [{money2 - float(money)}$]'
        user_dic['flow'].append(flow)

        # 4）保存用户字典
        db_handler.save(user_dic)
        msg =  f'用户 [{username}] 提现金额 [{money}] 成功，手续费为 [{money2 - float(money)}$]'
        bank_logger.info(msg)
        return True, msg
    else:
        msg = '余额不足，无法提现，请重新输入'
        bank_logger.warn(msg)
        return False, msg

# 还款接口
def repay_interface(username, money):
    user_dic = db_handler.select(username)
    user_dic['balance'] += money
    db_handler.save(user_dic)
    msg = f'用户 [{username}] 还款 [{money}] 成功'
    user_dic['flow'].append(msg)
    bank_logger.info(msg)
    return True, msg


# 转账接口
def transfer_interface(login_user, to_user, money):
    # 1. 获取当前用户字典
    login_user_dic = db_handler.select(login_user)

    # 2. 获取目标用户字典
    to_user_dic = db_handler.select(to_user)

    # 3. 判断目标用户是否存在
    if not to_user_dic:
        msg = '目标用户不存在'
        bank_logger.warn(msg)
        return False, msg

    # 4. 若目标用户存在，判断当前用户的余额是否足够
    if login_user_dic['balance'] >= money:
        # 若存在，则开始给目标用户转账
        login_user_dic['balance'] -= money
        # 记录转账流水
        login_user_flow = f'用户 [{login_user}] 给用户 [{to_user}] 转账：[{money}]$ 成功！'
        login_user_dic['flow'].append(login_user_flow)

        to_user_dic['balance'] += money
        # 记录接收流水
        to_user_flow = f'用户 [{to_user}] 接收用户 [{login_user}] 转账 [{money}]$ 成功！'
        to_user_dic['flow'].append(to_user_flow)
        db_handler.save(login_user_dic)
        db_handler.save(to_user_dic)
        msg = f'用户 [{login_user}] 给用户 [{to_user}] 转账 [{money}]$ 成功！'
        bank_logger.info(msg)
        return True, msg
    msg = '余额不足，无法转账'
    bank_logger.warn(msg)
    return False, msg

# 查看流水接口
def check_flow_interface(login_uer):
    user_dic = db_handler.select(login_uer)
    return user_dic.get('flow')

# 支付接口
def pay_interface(login_user, cost):
    user_dic = db_handler.select(login_user)
    cost = int(cost)
    # 判断用户钱是否足够
    if user_dic.get('balance') >= cost:
        user_dic['balance'] -= cost

        # 记录消费流水
        flow = f'用户消费金额：[{cost}$]'
        user_dic['flow'].append(flow)

        # 保存数据
        db_handler.save(user_dic)

        return True
    return False