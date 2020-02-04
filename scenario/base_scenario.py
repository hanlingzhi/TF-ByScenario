__author__ = 'hanlingzhi'

'''
create_date: 2019.12.5
usage: 场景基类
'''
import time, importlib
import inspect

from util import global_args
from util.constant import CONST


class BaseScenario(object):

    module_list = ()

    is_pass = (True, "default message")

    def __init__(self, uuid, logger):
        self.logger = logger
        self.id = uuid
        self.scene_args = global_args.get_value("args_dict_{}".format(uuid))
        self.logger.info("场景 {} 配置策略 ...".format(self.__class__.__name__.lower()))
        self.logger.debug("场景 {} 配置参数{} ...".format(self.__class__.__name__.lower(), self.scene_args))
        self.logger.debug("场景 {} module参数{} ...".format(self.__class__.__name__.lower(), self.module_list))

    def run(self):
        start = time.time()
        self.logger.info("场景 {} 执行开始 ...".format(self.__class__.__name__.lower()))
        prev_context = {}
        for m in self.module_list:
            module_name = "%s.%s" % (CONST.MODULE_NAME, m)
            module = importlib.import_module(module_name)
            cls_members = inspect.getmembers(module, inspect.isclass)
            for (name, _) in cls_members:
                c = getattr(module, name)
                if c.__base__.__name__ == "BaseModule":
                    self.logger.debug("加载模块类%s.%s" % (module_name, c.__name__))
                    c_instance = c(self.id, self.logger)
                    c_instance.__PRE_CONTEXT__(prev_context)
                    self.is_pass = c_instance.run()
                    prev_context = c_instance.__CONTEXT__()
            if not self.is_pass[0]:
                break
        end = time.time()
        self.logger.info(
            "场景 {} 执行结束, 执行结束，耗时:{}(s)".format(self.__class__.__name__.lower(), str(round((end - start), 2))))


    def sensor(self):
        if self.is_pass[0]:
            self.logger.info("场景 {} 自检程序成功 ...".format(self.__class__.__name__.lower()))
        else :
            self.logger.info("场景 {} 自检程序失败 ...".format(self.__class__.__name__.lower()))
            self.logger.error("失败原因:" + self.is_pass[1])
        return self.is_pass
