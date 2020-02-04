__author__ = 'hanlingzhi'

'''
create_date: 2019.12.5
usage: Const
'''

class _Const:
    class ConstError(TypeError):
        pass

    class ConstCaseError(ConstError):
        def __init__(self):
            pass

    def __setattr__(self, name, value):
        if not name.isupper():
            raise self.ConstCaseError(' Const "%s" must be uppercase ' % name)
        if name in self.__dict__:
            raise self.ConstError("Cannot modify %s value" % name)
        self.__dict__[name] = value


CONST = _Const()

CONST.PROJECT_NAME = 'ByScenarioTestFramework'

CONST.PROJECT_E_NAME = 'TF-ByScenario'

CONST.PROJECT_VERSION = '1.0'

CONST.SCENARIO_PATH = 'scenario'

CONST.MODULE_NAME = 'module'

# 日志常量配置
CONST.LOG_NAME = CONST.PROJECT_E_NAME + "_log"

CONST.LOG_BASE_PATH = 'logs'

CONST.LOG_FORMAT = '%(asctime)s [%(threadName)s] [%(name)s] [%(levelname)s] %(message)s'



