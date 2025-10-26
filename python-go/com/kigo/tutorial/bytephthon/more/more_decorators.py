"""
装饰器（Decorators）是应用包装函数的快捷方式。这有助于将某一功能与一些代码一遍又一
遍地“包装”。
举个例子，我为自己创建了一个 retry 装饰器，这样我可以将其运用到任何函
数之中，如果在一次运行中抛出了任何错误，它就会尝试重新运行，直到最大次数 5 次，并
且每次运行期间都会有一定的延迟。这对于你在对一台远程计算机进行网络调用的情况十分
有用：
"""
from functools import wraps
import logging
from time import sleep

logging.basicConfig()
log = logging.getLogger("retry")


def retry(f):
    @wraps(f)
    def wrapped_f(*args, **kwargs):
        MAX_ATTEMPTS = 5
        for attempt in range(1, MAX_ATTEMPTS + 1):
            try:
                return f(*args, **kwargs)
            except:
                log.exception("Attempt %s %s failed :| %s",
                              attempt,
                              MAX_ATTEMPTS,
                              (args, kwargs))
                sleep(10 * attempt)
        log.critical("All %s attempts failed : %s",
                     MAX_ATTEMPTS,
                     (args, kwargs))
    return  wrapped_f


counter = 0


@retry
def save_to_database(arg):
    print("Write to a database or make a network call or etc.")
    print("This will be automatically retried if exception is thrown.")
    global counter
    counter += 1
    # 这将在第一次调用时抛出异常
    # 在第二次运行时将正常工作（也就是重试）
    if counter < 2:
        raise ValueError(arg)


if __name__ == '__main__':
    save_to_database("Some bad value")