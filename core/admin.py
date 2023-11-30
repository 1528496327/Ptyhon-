from core import src
from interface import admin_interface
# 添加用户
def add_user():
    src.register()

# 修改用户额度
def change_balance():
    while True:
        # 1）输入修改额度和用户
        change_user = input('请输入要修改额度的用户名：').strip()
        money = input('请输入要修改的额度：').strip()
        if not money.isdigit():
            print('请输入正确的数字')
            continue
        money = int(money)
        # 2） 调用额度修改接口
        flag, msg = admin_interface.admin_modify_balance_interface(change_user, money)
        if float:
            print(msg)
            break
        else:
            print(msg)

    # 冻结账户
def lock_user():
    while True:
        # 1） 输入锁定的用户
        username = input('请输入需要冻结的用户名：').strip()
        flag, msg = admin_interface.lock_user_interface(username)
        if  flag:
            print(msg)
            break
        else:
            print(msg)

def admin_run():
    # 管理员功能字典
    func_dic = {
        '0': exit,
        '1': add_user,
        '2': change_balance,
        '3': lock_user,
    }

    while True:
        print("""
        0、退出
        1、添加账户
        2、修改额度
        3、冻结账户
        """)
        choice = input("请输入管理员功能编号：").strip()
        if choice not in func_dic:
          print('请输入正确的功能编号！')
          continue
        func_dic.get(choice)()

