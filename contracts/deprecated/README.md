# 历史合约归档

本目录保留早期资产管理、积分与结算功能的探索性合约，用于追踪项目演进。当前数据采集与存证链路不调用这些合约。

| 文件 | 历史用途 | 状态 |
|---|---|---|
| `SolarRWA.sol` | 资产管理原型 | 已归档 |
| `SolarToken.sol` | 积分合约原型 | 已归档 |
| `StableCoin.sol` | 结算合约原型 | 已归档 |

## 当前数据合约

当前数据存证使用 [`SolarDataStore.sol`](../SolarDataStore.sol)，包含 `storeData`、`getData`、`getLatestData` 和 `getDataCount` 等接口。合约保存物理指标与签名字符串，独立签名验证流程仍需完善。

项目介绍和当前实现状态见根目录 [README](../../README.md)。
