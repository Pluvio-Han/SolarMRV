# 安全策略 Security Policy

## 1. 密钥与敏感信息管理

### 1.1 严禁提交到公开仓库的内容

- `.env` / 各类 `*.env*` 文件（已加入 `.gitignore`）
- `data/wallets/` 下任何钱包 keystore（已加入 `.gitignore`）
- SM2 私钥、SM4 对称密钥、API Token、SSH 私钥、TLS 私钥
- 服务器登录凭证、第三方服务的访问令牌（含 Telegram Bot Token、云服务密钥等）

### 1.2 正确做法

1. 复制 `.env.example` 为 `.env` 并填入真实值
2. 在运行系统前执行 `set -a; source .env; set +a`，或通过部署环境注入变量
3. 部署服务器使用环境变量注入或托管的密钥管理服务（如阿里云 KMS、腾讯云 SSM）
4. **不要**在代码默认值里写入真实密钥

### 1.3 历史已暴露密钥的处理

早期版本曾在 `config.py` 默认值中包含明文 SM2 私钥与 Telegram Bot Token。这些值已存在于 git 公开历史中，必须：

1. **作废旧 SM2 密钥对**，重新生成新密钥并部署
2. 通过 BotFather 重置 Telegram Bot Token（如需继续使用）
3. 后续部署不再使用任何历史曝光的密钥

## 2. 数据隐私

- 设备采集数据可能涉及发电主体的运行规律，作为商业敏感信息处理
- 联盟链节点采用许可制接入，未经授权不开放公共查询
- 第三方核查接口（`api/verifier/`，开发中）将采用 API Key 鉴权 + 调用限流 + 全量审计日志
- 与外部主体的数据共享需签订数据使用边界协议

## 3. 漏洞披露

如发现安全漏洞，请：

1. **不要在 GitHub Issues 公开披露**
2. 通过 GitHub 仓库 owner 的联系方式或绑定邮箱进行私下披露
3. 描述漏洞复现步骤、影响范围、建议修复方向
4. 团队会在 72 小时内确认并启动修复流程

## 4. 已知问题（持续更新）

| 编号 | 问题 | 状态 |
|------|------|------|
| SEC-001 | 早期 `config.py` 在默认值中暴露过 SM2 私钥（git 历史保留） | 已修补：默认值移除 / 当前以环境变量注入 / 待重新生成密钥 |
| SEC-002 | `data/wallets/user_wallet.json` 历史上曾被 git 跟踪 | 已修补：从跟踪移除 + 加入 .gitignore |
| SEC-003 | 单节点联盟链部署，缺少多方共识背书 | 计划中：02 代码计划 P1 多节点联盟链联调 |

## 5. 联系方式

- GitHub Issues（非安全问题）：https://github.com/Pluvio-Han/SolarMRV/issues
- 安全漏洞披露：请通过仓库 owner 私下联系
