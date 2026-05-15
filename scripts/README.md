# Scripts

这里存放需要人工执行的运维、设备控制和报告生成脚本。

常用示例：

```bash
bash scripts/start_nodes.sh
python scripts/turn_on_light.py
python scripts/generate_report_html.py
```

`start_nodes.sh` 会通过 SSH 操作远程节点；执行前请确认目标服务器和密钥环境。
