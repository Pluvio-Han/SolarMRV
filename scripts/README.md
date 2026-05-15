# Scripts

本目录存放需要人工执行的辅助脚本，分为两类：

## 1. 通用运维与工具脚本（本目录根级）

| 脚本 | 类型 | 用途 |
|------|------|------|
| `start_nodes.sh` | Bash | 通过 SSH 启动远程 FISCO-BCOS 节点 |
| `turn_on_light.py` | Python | 设备端测试：开启负载（灯泡）|
| `generate_report_html.py` | Python | 从采集数据生成 HTML 监控报告 |

## 2. 联盟链运维子目录 `chain-ops/`

存放 9 个 FISCO-BCOS 节点运维 shell 脚本（节点重启、重建、清理、P2P 修复等），详见 [`chain-ops/README.md`](chain-ops/README.md)。

> 这些原本错放在 `tests/` 目录，本次合规重构期间统一归类。它们**不是测试**而是运维操作。

## 注意事项

- 大部分脚本会通过 SSH 操作远程节点，执行前请确认 `.env` 中的 `CHAIN_HOST` / `CHAIN_USER` 与 SSH 密钥环境正确
- 当前云端部署基础设施已下线归档，部分脚本中的硬编码 IP / 路径需要根据新部署环境调整
- 部分链运维脚本（如 `chain-ops/test_nuke.sh`）会**清空节点数据**，使用前务必确认
