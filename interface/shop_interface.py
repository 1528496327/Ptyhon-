"""
购物商城接口
"""
from db import db_handler
from lib import common
shop_logger = common.get_logger('shop')

# 商品结算支付接口
def shopping_interface(login_user, shopping_car):
    # 1）计算消费总额
    # {'商品名称': []}
    cost = 0
    for price_number in shopping_car.values():
        price, number = price_number

        cost += (price * number)

    # 2）导入银行接口
    from interface import bank_interface
    # 3）逻辑校验成功后，再调用银行的支付接口
    flag = bank_interface.pay_interface(login_user, cost)
    if flag:
        msg = '支付成功，准备发货！'
        shop_logger.info(msg)
        return True, msg
    else:
        msg =  '支付失败，金额不足'
        shop_logger.warn(msg)
        return False, msg

# 购物车添加接口
def add_shop_car_initerface(login_user, shopping_car):
    # 1) 获取当前用户的购物车
    user_dic = db_handler.select(login_user)
    shop_car = user_dic.get('shop_car')
    # 2）添加购物车
    # 2.1）判断当前用户选择的商品，是否已经存在
    for shop_name, price_number in shopping_car.items():
        # 每个商品的数量
        number = price_number[1]
        #2.2）若商品存在，累加商品数量
        if shop_name in shop_car:
            user_dic['shop_car'][shop_name][1] += int(number)
            # 2.3）若不是重复的，更新到商品字典中
        else:
            user_dic['shop_car'].update(
                {shop_name: price_number}
            )
    db_handler.save(user_dic)
    msg = '添加购物车成功'
    shop_logger.info(msg)
    return True, msg

# 查看购物车接口
def check_shop_car_interface(login_user):
    user_dic = db_handler.select(login_user)
    return user_dic.get('shop_car')
