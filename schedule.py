__author__ = 'hanlingzhi'

"""
create_date: 2019.12.5
usage: schedule
"""

import traceback
import importlib
import inspect
import time

from util.constant import CONST
from util.get_ip import get_host_ip

class Schedule(object):

    # scenario finish flag
    is_finish = False
    # scenario result flag
    is_pass = True
    # scenario result
    result = ''

    scenario_instance = object

    def __init__(self, name, uuid, logger, retry=0, count=1, ci=''):
        self.scenario_name = name
        self.id = uuid
        self.logger = logger
        self.retry = retry
        self.count = count
        self.ci = ci
        self.logger.info("执行机器IP {}".format(get_host_ip()))
        self.logger.info("调度器加载 {} 场景的执行策略 ...".format(self.scenario_name))
        self.start = time.time()

    def show_attr(self):
        att_list = list(filter(lambda x: not str(x).startswith("__") and not callable(getattr(self, x)), dir(self)))
        att_dict = {x: getattr(self, x) for x in att_list}
        self.logger.debug("调度器实例的属性参数 {} ...".format(att_dict))

    def exc(self):
        self.logger.info("调度器开始执行 {} 场景的脚本 ...".format(self.scenario_name))
        self.show_attr()
        for i in range(0, self.count):
            r = self.retry
            self.logger.info("执行 {} 场景第{}次 ...".format(self.scenario_name, i + 1))
            while r >= 0:
                if not self.is_pass:
                    self.logger.warning("执行 {} 场景出错, 重试第{}次 ...".format(self.scenario_name, self.retry - r))
                try:
                    self.get_classes()
                    self.scenario_instance.run()
                    re = self.scenario_instance.sensor()
                    self.is_pass = re[0]
                    self.result = "{}\n({}) {}".format(self.result, str(i + 1), str(re[1]))
                    if self.is_pass:
                        break
                except Exception as e:
                    # catch exception to retry
                    traceback.print_exc()
                    self.is_pass = False
                    self.result = "{}\n({}) {}".format(self.result, i + 1, str(e))
                    if r == 0:
                        self.logger.error("执行 {} 场景失败 ...".format(self.scenario_name))
                        break
                r -= 1
            time.sleep(2)
        self.scenario_instance = None
        self.is_finish = True
        self.finish_call_back()

    def get_classes(self):
        module_name = "%s.%s" % (CONST.SCENARIO_PATH, self.scenario_name)
        module = importlib.import_module(module_name)
        cls_members = inspect.getmembers(module, inspect.isclass)
        for (name, _) in cls_members:
            c = getattr(module, name)
            # check inherit and new instance
            if c.__base__.__name__ == "BaseScenario":
                self.logger.debug("加载场景类 %s.%s" % (module_name, c.__name__))
                self.scenario_instance = c(self.id, self.logger)
            else:
                del c

    def finish_call_back(self):
        if self.is_finish:
            self.logger.info("ci = {}".format(self.ci))
            # upload report
            self.logger.info("调度器上报结果 结果 {} ...".format(self.result))
