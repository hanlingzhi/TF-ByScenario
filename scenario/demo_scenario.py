__author__ = 'hanlingzhi'

'''
create_date: 2019.12.5
usage: demo
'''

from scenario.base_scenario import BaseScenario

class DemoScenario(BaseScenario):

    # 定义场景执行的编排队列
    module_list = ('module1', 'module2',)

    


