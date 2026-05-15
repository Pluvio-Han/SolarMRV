# Tests

本目录存放项目测试脚本。

## 目录结构

- `conftest.py` — pytest 公共配置（路径注入、共享 fixture）
- `test_*.py` — 单元 / 集成测试用例
- `deprecated/` — 已停用的早期测试（含旧 RWA / DEX / 铸币相关用例与 utils 调试脚本归档）

## 运行方式

```bash
# 全量运行
pytest -v

# 按标记运行
pytest -m unit          # 仅运行单元测试
pytest -m integration   # 集成测试（需链节点 / 串口）
pytest -m "not slow"    # 跳过慢测试

# 单文件
python tests/test_chain_client.py    # 直接执行（含路径兼容逻辑）
pytest tests/test_chain_client.py    # 或通过 pytest
```

## 注意事项

- 部分测试需要连接真实链节点、设备串口或远程服务器，运行前请确认 `.env` 配置正确
- 链运维脚本（重启 / 重建 / 修复 P2P 等）已移至 `scripts/chain-ops/`，那些**不是测试**而是运维操作
- 新增测试请遵循 `test_*.py` 命名规范并加上合适的 `@pytest.mark.*` 标记

## 当前测试覆盖范围（待补齐）

| 模块 | 覆盖率 | 备注 |
|------|--------|------|
| `chain_client.py` | 部分 | 多个 `test_chain_*.py` 提供链交互验证 |
| `solar_monitor.py` | 0% | 待新建单元测试 |
| `mrv/` (待建) | 0% | 待 P0 建设完成后补 |
| `api/verifier/` (待建) | 0% | 待 P0 建设完成后补 |

后续计划详见 [`最新执行计划/02_代码与技术执行计划.md`](../最新执行计划/02_代码与技术执行计划.md) 第二档 P1.8 "自动化测试与 CI"。
