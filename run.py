__author__ = 'hanlingzhi'

"""
create_date: 2019.12.5
usage: main
"""

import argparse, ast, os

from util.constant import CONST
from util import global_args
from util.log import LogUtil
from util import uuid
from schedule import Schedule


class SceneAction(argparse.Action):
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        if nargs is not None:
            raise ValueError("args not allowed")
        super(SceneAction, self).__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        """ scenario exists in $PROJECT/scenario/$name.py """
        path = os.path.join(os.getcwd(), CONST.SCENARIO_PATH)
        scene_list = [f.split('.')[0] for f in list(filter(lambda x: str(x).endswith(".py"), os.listdir(path)))]
        if values not in scene_list:
            raise ValueError("No scenario exists, Pls create a scenario first ...")
        setattr(namespace, self.dest, values)


if __name__ == '__main__':
    # create Parser
    parser = argparse.ArgumentParser(prog='run',
                                     description='%sV%s' % (CONST.PROJECT_NAME, CONST.PROJECT_VERSION))
    # add args
    parser.add_argument('--name', type=str, required=True, help='scenario name', dest="scenario", action=SceneAction)
    parser.add_argument('--args', type=str, required=True, help='scenario args(json)', dest='args_json')
    parser.add_argument('-d', action='store_true', help='debug mode', dest='is_debug')
    parser.add_argument('-r', type=int, help='retry times', default=0, dest='retry_time')
    parser.add_argument('--count', type=int, help='execute times', default=1, dest='count')
    parser.add_argument('--ci', type=str, help='CI args(json)', default='{}', dest='ci')
    args = parser.parse_args()
    # set global vars
    uuid = uuid.short_uuid()
    global_args.set_value("uuid", uuid)
    # set debug mode
    global_args.set_value("is_debug", args.is_debug)
    # args json to dict
    global_args.set_value("args_dict_{}".format(uuid), ast.literal_eval(args.args_json))
    # set log level
    data_logger = LogUtil(CONST.PROJECT_E_NAME)
    data_logger.debug('cmdline args: {}'.format(args))
    # set and run schedule
    Schedule(args.scenario, uuid, data_logger, args.retry_time, args.count, args.ci).exc()
