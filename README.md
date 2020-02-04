# TF-ByScenario
A self-developed testing framework based on scenario driven/module arrangement。

基于场景驱动/模块编排的的自研测试框架。

# 工程结构说明
<pre>
.
├── README.md
├── __init__.py
├── logs
│   └── __init__.py
├── module
│   ├── __init__.py
│   ├── base_module.py
│   ├── module1.py
│   └── module2.py
├── run.py
├── scenario
│   ├── __init__.py
│   ├── base_scenario.py
│   └── demo_scenario.py
├── schedule.py
└── util
    ├── constant.py
    ├── get_ip.py
    ├── global_args.py
    ├── log.py
    └── uuid.py
</pre>
*******

# CMDLINE

usage: run [-h] --name SCENARIO --args ARGS_JSON [-d] [-r RETRY_TIME] [--count COUNT] [--ci CI]

ByScenarioTestFramework V1.0

<pre>
optional arguments:
  -h, --help        show this help message and exit
  --name SCENARIO   scenario name
  --args ARGS_JSON  scenario args(json)
  -d                debug mode
  -r RETRY_TIME     retry times
  --count COUNT     execute times
  --ci CI           CI args(json)
</pre>

* 本地运行的例子:
<pre>python3 run.py --name demo_scenario --args "{'id':2}"</pre>
* 本地调式的例子:
<pre>python3 run.py --name demo_scenario --args "{'id':2}" -d </pre>
* CI集成的例子:
<pre>python3 run.py --name demo_scenario --args "{'id':2}" --count 1 -r 0 --ci "{'plat_id':'45' ...}"</pre>

# 注意事项
* module开发必须在module目录下, 且一定要继承 BaseModule
* Scene开发必须在scenario目录下, 且一定要继承 BaseScenario
* --name 实参值, 必须在scenario目录中是存在的python文件

# module上下文传递
提供两种方式：
* (1) 每个场景都有独立的全局变量域，args_dict_{uuid}，可以将单场景的全局变量保存其中。
* (2) 每个module会获取前一个(无法追溯更早)module的上文实例属性，需要设置可继承的context_attr_list('属性1','属性2')的属性列表，然后可以在module中通过self.属性1 访问。
如果要传递给下文，一定要赋值到当前实例属性中。

# sensor
module提供了sensor的方法, 每一个module需要override
<pre>
    # 定义自检程序
    def sensor(self):
        return True/False, "返回的结果文案"
</pre>
sensor的作用：
* (1) module结果自检, 有些场景不会抛异常, 但是结果已经不对了。除了被动的捕获异常, 也需要主动的检测。
* (2) module的最终返回结果定义文案, 会在回调返回中进行展示。
