#!/bin/bash
set -e

# FISCO-BCOS 一键部署脚本 (Ubuntu)
# 适配腾讯云/阿里云环境 (使用 Gitee 源加速)

echo "🛠️ [1/4] 更新系统并安装依赖 (Java, OpenSSL, Curl)..."
sudo apt-get update
sudo apt-get install -y default-jdk openssl curl git tree

echo "📥 [2/4] 下载建链脚本 (从 Gitee 镜像)..."
mkdir -p ~/fisco && cd ~/fisco
curl -#LO https://gitee.com/FISCO-BCOS/FISCO-BCOS/raw/master/tools/build_chain.sh
chmod u+x build_chain.sh

echo "⛓️ [3/4] 搭建 4 节点联盟链..."
# -l: 指定 IP (本地环回) 和 节点数 (4个)
# -p: 指定起始端口 (P2P:30300, Channel:20200, RPC:8545)
bash build_chain.sh -l 127.0.0.1:4 -p 30300,20200,8545

echo "🚀 [4/4] 启动所有节点..."
bash nodes/127.0.0.1/start_all.sh

echo "✅ 部署完成！节点进程如下："
ps -ef | grep -v grep | grep fisco-bcos

echo "---------------------------------------------------"
echo "🌐虽然节点在云端运行，但我们需要从 Mac 远程连接它。"
echo "请确保防火墙已放行端口: 20200 (SDK), 30300 (P2P), 8545 (Console)"
echo "---------------------------------------------------"
