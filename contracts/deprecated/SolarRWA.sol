// ============================================================================
// DEPRECATED 2026-02：本合约属于项目早期原型阶段产物。结合 2026 年初监管环境变化（参见
// 八部门关于现实世界资产代币化业务的政策口径），项目已主动剥离全部金融化属性。本文件不再
// 部署、不再调用，仅作为早期技术原型阶段的代码留痕。
// 当前在用合约：contracts/SolarDataStore.sol（纯数据存证，不涉及任何价值转移逻辑）。
// 当前项目定位：分布式光伏 MRV（监测—报告—核查）可信数据底座。
// ============================================================================

pragma solidity ^0.4.25;

interface ISolarToken {
    function mint(address _to, uint256 _amount) external returns (bool);
    function balanceOf(address _owner) external view returns (uint256);
    function transferFrom(address _from, address _to, uint256 _value) external returns (bool);
}

interface IStableCoin {
    function transferFrom(address _from, address _to, uint256 _value) external returns (bool);
    function balanceOf(address _owner) external view returns (uint256);
}

/**
 * @title SolarRWA - RWA核心逻辑合约
 * @dev 负责管理硬件设备、将发电量铸造为绿电代币、并提供绿电交易市场
 */
contract SolarRWA {
    address public owner;
    ISolarToken public solarToken;
    IStableCoin public stableCoin;

    // 定价：1 SLG = 1 mUSD （方便测试，按相同精度 1:1 兑换）
    uint256 public exchangeRate = 1;

    struct Device {
        address ownerWallet;
        uint256 lastTotalEnergy; // 上次入账的累计发电量 (放大100倍的值，即 100 = 1 kWh)
        bool isRegistered;
    }

    // 设备ID => 设备信息 (在 0.4.25 下, 动态大小键 mapping 不能声明为 public, 需要手写 getter)
    mapping(string => Device) devices;

    function getDevice(string deviceId) public view returns (address ownerWallet, uint256 lastTotalEnergy, bool isRegistered) {
        Device storage d = devices[deviceId];
        return (d.ownerWallet, d.lastTotalEnergy, d.isRegistered);
    }

    // 总铸造的代币数量
    uint256 public totalMintedSLG;

    // 事件录像，FISCO-BCOS 会将其永久存储到日志数据库
    event DeviceRegistered(string deviceId, address ownerWallet);
    event DataStoredAndMinted(string deviceId, uint256 currentTotalEnergy, uint256 energyDelta, uint256 mintedTokens);
    event TokensPurchased(address buyer, address seller, uint256 slgAmount, uint256 mUsdAmount);

    constructor(address _solarTokenAddress, address _stableCoinAddress) public {
        owner = msg.sender;
        solarToken = ISolarToken(_solarTokenAddress);
        stableCoin = IStableCoin(_stableCoinAddress);
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner can call this");
        _;
    }

    /**
     * @dev 1. 注册设备：将物理设备的唯一ID绑定到用户的 Web3 钱包
     */
    function registerDevice(string deviceId, address ownerWallet) public onlyOwner {
        require(!devices[deviceId].isRegistered, "Device already registered");
        require(ownerWallet != address(0), "Invalid wallet address");

        devices[deviceId] = Device({
            ownerWallet: ownerWallet,
            lastTotalEnergy: 0,
            isRegistered: true
        });

        emit DeviceRegistered(deviceId, ownerWallet);
    }

    /**
     * @dev 2. 核心预言机入口：接收来自硬件的真实发电数据，若有增量，则为物理设备拥有者铸造对应的 SolarToken
     * @param deviceId 设备唯一标识
     * @param totalEnergy 当前的累计发电量 (因为 Python 传上来的是放大 100 倍的整数，比如 100 代表 1 kWh)
     */
    function storeDeviceData(string deviceId, uint256 totalEnergy) public onlyOwner {
        require(devices[deviceId].isRegistered, "Device not registered");

        Device storage device = devices[deviceId];
        
        // 计算本次增发的电量 (自上次记录以来的实际发出的绿电增量)
        uint256 energyDelta = 0;
        if (totalEnergy > device.lastTotalEnergy) {
            energyDelta = totalEnergy - device.lastTotalEnergy;
        }

        uint256 tokensToMint = 0;
        if (energyDelta > 0) {
            // 比例锚定：每发 1 kWh (在底层代表数字 100) 赠送 1 枚 SLG 代币 (包含 18 位 decimals)
            // 即 energyDelta 是 100 时，要铸造 1 * 10^18 个 Token
            // 所以 tokensToMint = (energyDelta / 100) * 10^18 = energyDelta * 10^16
            tokensToMint = energyDelta * (10 ** 16);
            
            // 调用 SolarToken 合约的 mint 方法（本合约必须已被白名单授权为 Minter）
            require(solarToken.mint(device.ownerWallet, tokensToMint), "Mint failed");
            
            device.lastTotalEnergy = totalEnergy;
            totalMintedSLG += tokensToMint;
        }

        // 触发上链存证日志
        emit DataStoredAndMinted(deviceId, totalEnergy, energyDelta, tokensToMint);
    }

    /**
     * @dev 3. DApp 积分交易去中心化市场 (微型 DEX)：使用 StableCoin (mUSD) 购买他人的 SolarToken (SLG)
     * 要求:
     * - 调用者 (买家) 必须先调用 StableCoin 的 approve 方法授权本 RWA 合约扣款
     * - 卖家 (seller) 必须先调用 SolarToken 的 approve 方法授权本 RWA 合约划转绿电
     */
    function buyGreenTokens(address seller, uint256 slgAmount) public {
        uint256 mUsdCost = slgAmount * exchangeRate;
        
        require(stableCoin.balanceOf(msg.sender) >= mUsdCost, "Buyer has insufficient mUSD");
        require(solarToken.balanceOf(seller) >= slgAmount, "Seller has insufficient SLG");

        // 1. 扣除买家的测试法币，转移给卖家
        require(stableCoin.transferFrom(msg.sender, seller, mUsdCost), "mUSD payment transfer failed");
        
        // 2. 扣除卖家的绿电积分，转移给真正的绿色买家
        require(solarToken.transferFrom(seller, msg.sender, slgAmount), "SLG energy delivery failed");

        emit TokensPurchased(msg.sender, seller, slgAmount, mUsdCost);
    }
}
