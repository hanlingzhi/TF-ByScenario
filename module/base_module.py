__author__ = 'hanlingzhi'

'''
create_date: 2019.12.5
usage: 场景基类
'''
import time

from util import global_args

class BaseModule(object):

    function_list = ()

    context_attr_list = ()

    def __init__(self, uuid, logger):
        self.logger = logger
        self.module_args = global_args.get_value("args_dict_{}".format(uuid))
        self.logger.info("模块 {} 配置策略 ...".format(self.__class__.__name__.lower()))
        self.logger.debug("模块 {} 配置参数 {} ...".format(self.__class__.__name__.lower(), self.module_args))
        self.logger.debug("模块 {} function参数 {} ...".format(self.__class__.__name__.lower(), self.function_list))

    def run(self):
        return self.__DO__()

    def __DO__(self):
        list(map(self.__EXE__, self.function_list))
        # 调用自检检查
        return self.sensor()

    def __EXE__(self, method_name):
        self.logger.info("----- 开始执行[%s].%s()" % (self.__class__.__name__, method_name))
        start = time.time()
        m = getattr(self, method_name)
        m()
        end = time.time()
        self.logger.info(
            "----- 执行结束[%s].%s()，耗时：" % (self.__class__.__name__, method_name) + str(round((end - start), 2)) + "(s)")

    def __CONTEXT__(self):
        att_list = list(filter(lambda x: not str(x).startswith("__") and not callable(getattr(self, x)), dir(self)))
        att_dict = {x: getattr(self, x) for x in att_list}
        self.logger.debug("模块实例的属性参数 {} ...".format(att_dict))
        return att_dict

    def __PRE_CONTEXT__(self, context):
        for attr in self.context_attr_list:
            if attr in context.keys() or attr in self.module_args.keys():
                if attr in context.keys():
                    setattr(self, attr, context[attr])
                else:
                    setattr(self, attr, self.module_args[attr])
            else:
                assert False, "获取不到传参或者上文属性 {} ...".format(attr)
        att_list = list(filter(lambda x: not str(x).startswith("__") and not callable(getattr(self, x)), dir(self)))
        att_dict = {x: getattr(self, x) for x in att_list}
        self.logger.debug("模块实例的属性参数 {} ...".format(att_dict))

    def sensor(self):
        self.logger.info("模块 {} 自检程序执行中 ...".format(self.__class__.__name__.lower()))
        return True, "默认的结果文案"
