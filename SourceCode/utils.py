import os
import psutil
import time

def memLog(func):
    """
    内存检视装饰器
    在函数定义时在上方加上@memLog，执行函数时可以检视python运行内存
    """
    def wrapper(*args, **kw):
        print(u'运行前的的内存使用：%.4f MB' % (psutil.Process(os.getpid()).memory_info().rss / 1024 /1024) )
        result = func(*args, **kw)
        print(u'运行后的内存使用：%.4f MB' % (psutil.Process(os.getpid()).memory_info().rss / 1024 /1024) )
        return result
    return wrapper

def timeLog(func):
    """
    运行时间检视装饰器
    在函数定义时在上方加上@timeLog，执行函数时可以记录函数运行时间
    """
    def wrapper(*args, **kw):
        t0 = time.time()
        result = func(*args, **kw)
        t1 = time.time()
        print("当前函数运行时间：%.5f s"%(t1-t0))
        return result
    return wrapper