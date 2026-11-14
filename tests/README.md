# 手工联调脚本

本目录主要保存硬件和链节点的手工联调入口。现有 `test_*.py` 尚未整理为标准自动化测试，部分脚本在加载时会直接连接串口、SSH 或链节点。请按用途选择单个脚本，并在运行前检查环境配置。

| 文件 | 联调用途 |
|---|---|
| `test_raw.py`、`test_payload.py` | 原始采集与数据包检查 |
| `test_sig.py`、`test_upload.py`、`test_chain_client.py` | 签名生成和链上写入 |
| `test_chain_latest.py`、`test_chain_history.py` | 链上记录查询 |
| `test_chain_status.py`、`test_chain_sealers.py`、`test_txpool.py` | 节点、共识与交易池状态 |
| `test_chain_final.py` | 链连接与查询检查 |
| `test_ssh.py`、`test_unlock.py` | 远程连接与账户状态检查 |
| `full_test.py` | 采集、签名、记录、图表、上链与通知联调 |
| `conftest.py` | 路径和后续自动化测试的共享配置 |

示例：

```bash
python tests/test_chain_client.py
```

写入类脚本会产生链上记录，通知类流程可能发送 Telegram 消息。`full_test.py` 的末尾提示尚不能替代逐步骤结果核对。后续验证方式见[技术路线](../docs/roadmap.md)。
