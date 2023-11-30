# 面条版
"""
def register():
    while True:
        # 1）让用户输入用户名与密码，进行校验
        username = input('请输入用户名：').strip()
        password = input('请输入密码：').strip()
        re_password = input('请确认密码：').strip()

        # 小的逻辑处理：比如两次密码是否一致
        if password == re_password:
            import json
            import os
            from conf import settings
            user_path = os.path.join(
                settings.USER_DATA_PATH, f'{username}.json'
            )
            # 接收到注册之后的结果，并打印
            # 2）查看用户是否存在
            if os.path.exists(user_path):
                print('请重新输入！')

                with open(user_path, 'r', encoding='utf-8') as f:
                    user_dic = json.load(f)

                if user_dic:
                    print('用户已存在，请重新输入！')
                    continue

            # 3）用户名存在，让用户重新输入
            # 4）用户名不存在，保存用户数据
            # 4.1）组织用户的数据的字典信息
            user_dic = {
                'username': username,
                'password': password,
                'balance': 15000,
                'flow': [],  # 用于记录用户流水的列表
                'shop_car': {},  # 用于记录用户的购物车
                'locked': False  # 用于记录用户是否被冻结， False未冻结，True已冻结
            }

            # 一个用户应该拥有一个数据文件,文件名格式为  user.json
            # 4.2）拼接用户的json文件路径
            user_path = os.path.join(
                settings.USER_DATA_PATH, f'{username}.json'
            )
            with open(user_path,'w',encoding='utf-8') as f:
                json.dump(user_dic,f,ensure_ascii=False)  # ensure_ascii=False让文件中的中文显示
                """