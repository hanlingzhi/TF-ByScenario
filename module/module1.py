__author__ = 'hanlingzhi'

'''
create_date: 2019.12.5
usage: demo module

'''

from module.base_module import BaseModule

class Module1(BaseModule):

    function_list = ('test_action_a', 'test_action_b',)

    context_attr_list = ('id',)

    order_id = 0

    def test_action_a(self):
        self.logger.info("外部传参id=%s" % self.id)
        assert self.id >0, "id数据传递不合法"

    def test_action_b(self):
        self.order_id = 122
        pass

    def test_action_c(self):
        pass

    # 定义自检程序
    def sensor(self):
        return True, "处理ID={}数据正常 ...".format(self.id)
