"""
存放用户视图层，核心逻辑
"""

from interface import user_interface
from interface import bank_interface
from interface import shop_interface
from lib import common

# 全局变量，记录用户是否已经登录
login_user = None

# 1、注册功能
# 分层版
def register():
    while True:
        # 1）让用户输入用户名与密码，进行校验
        username = input('请输入用户名：').strip()
        password = input('请输入密码：').strip()
        re_password = input('请确认密码：').strip()
        # 可以自定义金额
        # 小的逻辑处理：比如两次密码是否一致
        if password == re_password:
            # 2）调用接口层的注册接口，将用户名和密码交给接口层来处理
            flag, msg = user_interface.register_interface(
                username, password
            )
            # 3）根据flag判断用户是否注册成功
            if flag:
                print(msg)
                break
            else:
                print(msg)


# 2、登录功能
def login():
    # 登录视图
    while True:
        # 1）让用户输入用户名与密码
        username = input('请输入用户名：').strip()
        password = input('请输入密码：').strip()
        # 2）调用接口层，将数据传给登录接口
        flag, msg = user_interface.login_interface(
            username, password
        )
        if flag:
            print(msg)
            global login_user
            login_user = username
            break
        else:
            print(msg)

# 3、查看余额
@common.login_auth
def check_balance():
    # 直接调用查看余额接口，获取用户余额
    balence = user_interface.check_bal_interface(
        login_user
    )
    print(f'用户 {login_user} 账户余额为：{balence}')

# 4、提现功能
@common.login_auth
def withdraw():
    while True:
        # 1）让用户输入提现金额
        input_money = input('请输入提现金额：').strip()
        # 2）判断用输入的是否为数字
        if not input_money.isdigit():
            print('请重新输入金额数字')
            continue
        # 3）用户提现金额，将提现的金额交付给接口层来处理
        input_money = int(input_money)
        flag, msg = bank_interface.withdraw_interface(
            login_user, input_money
        )
        if flag:
            print(msg)
            break
        else:
            print(msg)

# 5、还款功能
@common.login_auth
def replay():
    while True:
        # 1）让用户输入还款金额
        input_money = input('请输出需要还款的金额：').strip()
        # 2）判断用户的输入是否是数字
        if not input_money.isdigit():
            print('请输入正确的金额')
            continue
        input_money = int(input_money)
        if input_money > 0:
            # 3）调用还款接口
            flag, msg = bank_interface.repay_interface(login_user, input_money)
            if flag:
                print(msg)
                break
        else:
            print('输入的金额不能小于0')

# 6、转账功能
@common.login_auth
def transfer():
    # 1）接收用户输入的 转账金额
    # 2）接收用户输入的 转账目标用户
    while True:
        to_user = input('请输入转账目标用户：').strip()
        money = input('请输入转账金额：').strip()
        # 判断用户输入的金额是否是数字或者 > 0
        if not money.isdigit():
            print('请输入正确的数字')
            continue

        money = int(money)
        if money >0:
            # 调用转账接口
            flag, msg = bank_interface.transfer_interface(login_user, to_user, money)
            if flag:
                print(msg)
                break
            else:
                print(msg)


# 7、查看流水
@common.login_auth
def check_flow():
    flow_list = bank_interface.check_flow_interface(login_user)
    if flow_list:
        for flow in flow_list:
            print(flow)
    else:
        print('当前用户暂无流水！')

# 8、购物功能
@common.login_auth
def shopping():
    # 不从文件中读取商品数据了，直接写（也可以从文件中读取商品）
    # 1）创建一个商品列表
    shop_list = [
        ['上海灌汤包', 30],
        ['weijc写真抱枕', 250],
        ['广东凤爪', 28],
        ['香港地道鱼丸', 15],
        ['macbook', 20000],
    ]

    # 初始化当前购物车：
    shopping_car = {}  # {'商品名称': ['单价', '数量']}

    # 2）枚举打印商品信息，让用户选择
    #    枚举：enumerate(可迭代对象)  ---> (可迭代对象的索引，索引对应的值)
    #    枚举：enumerate(可迭代对象)  ---> (0, ['上海灌汤包'， 30])

    while True:
        for index, shop in enumerate(shop_list):
            shop_name, shop_price = shop
            print(f'商品编号为：[{index}]',
                  f'商品名称：[{shop_name}]',
                  f'商品单价 ：[{shop_price}]')
        # 让用户选择
        choice = input('请输入商品编号来选择商品（输入 y 结账，n 添加至购物车）：').strip()

        # 输入 y 进入支付结算功能
        if choice == 'y':
            # 调用支付接口进行支付
            # 判断当前用户的购物车是否为空
            if not shopping_car:
                print('购物车为空，请添加商品！')
                continue
            flag, msg = shop_interface.shopping_interface(login_user,shopping_car)

            if flag:
                print(msg)
                break
            else:
                print(msg)
        # 输入 n 添加购物车
        elif choice == 'n':
            # 调用添加购物车接口
            flag, msg = shop_interface.add_shop_car_initerface(login_user, shopping_car)
            if flag:
                print(msg)
                break

        if not choice.isdigit():
            print('请输入正确编号！')
            continue
        choice = int(choice)

        # 3）判断choice是否存在
        if choice not in range(len(shop_list)):
            print('请输入正确编号！')
            continue

        # 4）获取商品名称与单价
        shop_name, shop_price = shop_list[choice]

        # 5）加入购物车
        # 5.1） 判断用户选择的商品是否重复，重复则数量 +1
        if shop_name in shopping_car:
            shopping_car[shop_name][1] += 1

        else:
            # 否则商品数量默认为1
            shopping_car[shop_name] = [shop_price, 1]
        print('当前购物车: ', shopping_car)

# 9、查看购物车
@common.login_auth
def check_shop_car():
    # 直接调用查看购物车接口
    shop_car = shop_interface.check_shop_car_interface(login_user)
    print(shop_car)
# 10、管理员功能
@common.login_auth
def admin():
    # 管理员功能
    from core import admin
    admin.admin_run()

# 创建函数功能字典
func_dic = {
    '0':exit,
    '1': register,
    '2': login,
    '3': check_balance,
    '4': withdraw,
    '5': replay,
    '6': transfer,
    '7': check_flow,
    '8': shopping,
    '9': check_shop_car,
    '10': admin,
}

# 视图层主程序
def run():
    while True:
        print('''
        ===== ATM + 购物车 =====
            0、退出
            1、注册功能
            2、登录功能
            3、查看余额
            4、提现功能
            5、还款功能
            6、转账功能
            7、查看流水
            8、购物功能
            9、查看购物车
            10、管理员功能
        =======   end   =======
        ''')

        choice = input('请输入功能编号：').strip()

        if choice not in func_dic:
            print('请输入正确的功能编号！')
            continue

        func_dic.get(choice)()
