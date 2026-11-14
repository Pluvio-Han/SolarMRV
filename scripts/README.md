# 设备辅助脚本

本目录保留当前硬件联调使用的辅助入口。

| 文件 | 用途 |
|---|---|
| [`turn_on_light.py`](turn_on_light.py) | 通过采集模块开启灯泡负载，检查设备侧写入操作 |

负载诊断工具见 [`utils/debug_load.py`](../utils/debug_load.py)，可读取蓄电池、光伏与负载状态，并尝试开启负载。两个工具均需真实串口设备，运行前应检查端口与设备参数。

日常采样与图表生成使用根目录 [`auto_monitor.py`](../auto_monitor.py)。
