# 联盟链运维脚本（chain-ops）

本目录归档项目早期 FISCO-BCOS 联盟链节点的运维操作脚本，原本错放在 `tests/` 目录中。这些**不是单元测试**，而是用于：

- 节点重启、重建、清理
- P2P 连接修复
- 节点身份信息查看
- 守护进程启动

## 文件说明

| 文件 | 用途 |
|------|------|
| `test_fix_p2p.sh` | P2P 连接故障修复 |
| `test_fix_p2p_dup.sh` | P2P 节点重复连接清理 |
| `test_nodeids.sh` | 查看节点 ID 列表 |
| `test_nuke.sh` | 完全清空节点（含数据）|
| `test_rebuild.sh` | 重建节点 |
| `test_rebuild2.sh` | 节点重建第二版（修复版）|
| `test_restart.sh` | 节点重启 |
| `test_restart_final.sh` | 节点重启最终版 |
| `test_start_detached.sh` | 后台启动节点 |

## ⚠️ 使用提示

- 这些脚本是早期开发阶段的工具，可能包含硬编码的服务器 IP、SSH 路径等
- 当前部署基础设施已下线归档（详见根目录 README 项目定位更新声明）
- 后续重新部署时建议参考但不直接复用，根据新环境改写
