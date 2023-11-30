"""
配置信息
"""
import os
# 获取项目根目录路径
BASE_PATH = os.path.dirname(os.path.dirname(__file__))


# 获取user_data 文件夹目录路径
USER_DATA_PATH = os.path.join(BASE_PATH, 'db', 'user_data')


# 日志配置文件
standard_format = '%(asctime)s - %(threadName)s:%(thread)d - 日志名字:%(name)s - %(filename)s:%(lineno)d -' \
                 '%(levelname)s - %(message)s'
simple_format = '[%(levelname)s][%(asctime)s][%(filename)s:%(lineno)d]%(message)s'
test_format = '%(asctime)s] %(message)s'

log_dir = os.path.join(BASE_PATH, 'log', 'atm.log')

# 日志配置字典
LOGGING_DIC = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {  # 不可以改，下面自定义了三种日志格式
        'standard': {  # 这是自己自定义的一种日志格式，可以更改
            'format': standard_format  # format 不可改  standard_format是个变量可以改
        },
        'simple': {
            'format': simple_format
        },
        'test': {
            'format': test_format
        },
    },
    'filters': {},
    # handlers是日志的接收者，不同的handler会将日志输出到不同的位置
    'handlers': {
        # 打印到终端的日志
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',  # 打印到屏幕
            'formatter': 'simple'
        },
        'default': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件
            # 'maxBytes': 1024*1024*5,  # 日志大小 5M
            'maxBytes': 1000,
            'backupCount': 5,
            'filename': log_dir,
            'encoding': 'utf-8',
            'formatter': 'standard',

        },
    },
    # loggers是日志的产生者，产生的日志会传递给handler然后控制输出
    'loggers': {
        '': {
            'handlers': ['default','console' ],  # 这里把上面定义的两个handler都加上，即log数据既写入文件又打印到屏幕
            'level': 'DEBUG',  # loggers(第一层日志级别关限制)--->handlers(第二层日志级别关卡限制)
            'propagate': False,  # 默认为True，向上（更高level的logger）传递，通常设置为False即可，否则会一份日志向上层层传递
        },
    },
}
