import multiprocessing
from tqdm import *
import time
import sys
import os

def err_call_back(err):
    print(f'出错啦~ error：{str(err)}')


# 封装的函数
def mk_test(height, width):
    # 计算相关系数和p值，并将结果写入新影像中
    position = multiprocessing.current_process().pid
    for i in trange(height, desc=f'进程{position}'):
        # for j in range(width):
        time.sleep(0.5)
    print(f'进程{position}完成')



# 多进程处理函数
def process_multiprocessing():
    # 创建进程池
    pool = multiprocessing.Pool(processes=6)

    for time in range(50,60):
        # 向进程池中添加要执行的任务
        pool.apply_async(mk_test, args=(time, time+1), error_callback=err_call_back)
    # 先调用close关闭进程池，不能再有新任务被加入到进程池中
    pool.close()

    # 用join函数等待所有子进程结束
    pool.join()
    print('joined')


# 主程序
if __name__ == '__main__':
    # 计算程序运行时间
    start = time.time()

    # 多进程处理
    process_multiprocessing()




    end = time.time()
    print("花了", (end - start) / 60, "分钟")
