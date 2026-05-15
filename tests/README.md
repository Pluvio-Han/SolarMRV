# Tests

这里存放从项目根目录归类过来的测试脚本，包括链状态、交易池、重启、节点、上传和设备通信测试。

早期 RWA / DEX / 铸币功能的测试脚本已归档至 `tests/deprecated/`，不再纳入运行流程。

这些 Python 测试文件已加入项目根目录路径兼容逻辑，可以从项目根目录运行：

```bash
python tests/test_chain_client.py
bash tests/test_restart.sh
```

部分测试会连接真实链节点、设备串口或远程服务器，运行前请确认配置和网络环境。
