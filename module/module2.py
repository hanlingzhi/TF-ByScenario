__author__ = 'hanlingzhi'

'''
create_date: 2019.12.5
usage: demo module

'''

from module.base_module import BaseModule

class Module1(BaseModule):

    function_list = ('test_action_e',)

    context_attr_list = ('id', 'order_id',)

    def test_action_e(self):
        self.logger.info("上文传递的order_id=%s" % self.order_id)
        # todo order something

    # 定义自检程序
    def sensor(self):
        return True, "处理订单ID={}数据正常 ...".format(self.order_id)
