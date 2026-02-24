// SPDX-License-Identifier: MIT
pragma solidity ^0.4.25;

/**
 * @title SolarDataStore - 光伏发电数据上链合约
 * @author PluvioHan
 * @notice 本合约用于将太阳能发电监测数据永久记录到区块链上
 * 
 * 核心功能:
 *   1. storeData()      - 存储一条光伏数据
 *   2. getData()        - 按ID查询某条数据
 *   3. getLatestData()  - 获取最新数据
 *   4. getDataCount()   - 获取总记录数
 */
contract SolarDataStore {

    // ============================================================
    //                    数据结构 (Struct)
    // ============================================================
    
    /*
     * 定义一条光伏数据的结构
     * struct 类似于 Python 的 dataclass 或 C 的 struct
     *
     * Solidity 小知识:
     *   - uint256 = 无符号整数 (0 到 2^256-1)
     *   - string  = 字符串
     *   - 链上数据一旦写入，永远无法删除或篡改!
     */
    struct SolarRecord {
        uint256 id;              // 记录编号 (自增)
        uint256 timestamp;       // 时间戳 (Unix 秒)
        uint256 pvPower;         // 光伏功率 (单位: 0.01W, 例如 565 = 5.65W)
        uint256 pvVoltage;       // 光伏电压 (单位: 0.01V, 例如 1839 = 18.39V)  
        uint256 battSOC;         // 电池电量 (单位: %, 例如 96)
        uint256 battVoltage;     // 电池电压 (单位: 0.01V, 例如 1380 = 13.80V)
        uint256 totalEnergy;     // 累计发电量 (单位: 0.01kWh, 例如 6 = 0.06kWh)
        string  signature;      // SM2 数字签名 (防篡改证明)
        address uploader;       // 上传者的区块链地址
    }

    // ============================================================
    //                    状态变量 (Storage)
    // ============================================================
    
    /*
     * Solidity 小知识:
     *   - 状态变量 = 永久存储在区块链上的数据 (类似数据库字段)
     *   - mapping  = 类似 Python 的 dict (键值对)
     *   - public   = 自动生成 getter 函数，外部可以直接读取
     */
    
    // 所有光伏记录: {0: Record, 1: Record, ...}
    mapping(uint256 => SolarRecord) public records;
    
    // 记录总数 (也是下一条记录的 ID)
    uint256 public recordCount;
    
    // 合约所有者 (部署合约的人)
    address public owner;

    // ============================================================
    //                    事件 (Event)
    // ============================================================
    
    /*
     * Solidity 小知识:
     *   - Event = 合约发出的"通知"，前端可以实时监听
     *   - emit  = 触发事件
     *   - indexed = 可以按这个字段过滤/搜索
     */
    event DataStored(
        uint256 indexed id,
        uint256 timestamp,
        uint256 pvPower,
        uint256 battSOC,
        address indexed uploader
    );

    // ============================================================
    //                    构造函数 & 修饰器
    // ============================================================
    
    // 构造函数 - 合约部署时自动执行一次 (类似 Python 的 __init__)
    constructor() public {
        owner = msg.sender;  // msg.sender = 部署合约的人的地址
        recordCount = 0;
    }

    // 修饰器 - 限制只有 owner 才能调用某些函数 (类似 Python 装饰器)
    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner can call this");
        _;  // 下划线 = 继续执行被修饰的函数体
    }

    // ============================================================
    //                    写入函数 (Write)
    // ============================================================

    /*
     * 存储一条光伏监测数据到链上
     *
     * 为什么参数要放大100倍?
     *   Solidity 不支持小数 (float)! 
     *   所以 5.65W 要存成 565，读取时再除以 100
     */
    function storeData(
        uint256 _pvPower,
        uint256 _pvVoltage,
        uint256 _battSOC,
        uint256 _battVoltage,
        uint256 _totalEnergy,
        string _signature
    ) public {
        // 创建新记录并存入 mapping (0.4.25 使用位置参数，顺序须与 struct 定义一致)
        records[recordCount] = SolarRecord(
            recordCount,           // id
            block.timestamp,       // timestamp
            _pvPower,              // pvPower
            _pvVoltage,            // pvVoltage
            _battSOC,              // battSOC
            _battVoltage,          // battVoltage
            _totalEnergy,          // totalEnergy
            _signature,            // signature
            msg.sender             // uploader
        );

        // 触发事件 (前端可以监听到)
        emit DataStored(recordCount, block.timestamp, _pvPower, _battSOC, msg.sender);

        // 计数器 +1
        recordCount++;
    }

    // ============================================================
    //                    查询函数 (Read / View)
    // ============================================================
    
    /*
     * Solidity 小知识:
     *   - view    = 只读函数，不修改链上数据，不消耗 gas
     *   - returns = 声明返回值类型
     */

    // 按 ID 查询某条记录
    function getData(uint256 _id) public view returns (
        uint256 id,
        uint256 timestamp,
        uint256 pvPower,
        uint256 pvVoltage,
        uint256 battSOC,
        uint256 battVoltage,
        uint256 totalEnergy,
        string signature,
        address uploader
    ) {
        require(_id < recordCount, "Record does not exist");
        SolarRecord storage r = records[_id];
        return (
            r.id, r.timestamp, r.pvPower, r.pvVoltage,
            r.battSOC, r.battVoltage, r.totalEnergy,
            r.signature, r.uploader
        );
    }

    // 获取最新一条记录
    function getLatestData() public view returns (
        uint256 id,
        uint256 timestamp,
        uint256 pvPower,
        uint256 pvVoltage,
        uint256 battSOC,
        uint256 battVoltage,
        uint256 totalEnergy,
        string signature,
        address uploader
    ) {
        require(recordCount > 0, "No data yet");
        return getData(recordCount - 1);
    }

    // 获取总记录数
    function getDataCount() public view returns (uint256) {
        return recordCount;
    }

    // ============================================================
    //                    管理函数 (Admin)
    // ============================================================

    // 转让合约所有权 (onlyOwner 确保只有当前 owner 能调用)
    function transferOwnership(address _newOwner) public onlyOwner {
        require(_newOwner != address(0), "Invalid address");
        owner = _newOwner;
    }
}
