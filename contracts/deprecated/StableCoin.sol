// ============================================================================
// DEPRECATED 2026-02：本合约属于项目早期原型阶段产物。结合 2026 年初监管环境变化（参见
// 八部门关于现实世界资产代币化业务的政策口径），项目已主动剥离全部金融化属性。本文件不再
// 部署、不再调用，仅作为早期技术原型阶段的代码留痕。
// 当前在用合约：contracts/SolarDataStore.sol（纯数据存证，不涉及任何价值转移逻辑）。
// 当前项目定位：分布式光伏 MRV（监测—报告—核查）可信数据底座。
// ============================================================================

pragma solidity ^0.4.25;

/**
 * @title StableCoin
 * @dev 基本的ERC20代币实现 (适用 FISCO-BCOS 0.4.25)
 * 用于模拟与法币锚定的支付货币 (1 USD = 1 Token)
 */
contract StableCoin {
    string public name;
    string public symbol;
    uint8 public decimals;
    uint256 public totalSupply;

    mapping(address => uint256) public balances;
    mapping(address => mapping(address => uint256)) public allowed;

    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);
    event Faucet(address indexed to, uint256 amount);

    constructor() public {
        name = "Mock USD Token";
        symbol = "mUSD";
        decimals = 18;
        // 初始发行 1000 万 个 mUSD 给部署者
        totalSupply = 10000000 * (10 ** uint256(decimals));
        balances[msg.sender] = totalSupply;
        emit Transfer(address(0), msg.sender, totalSupply);
    }

    function balanceOf(address _owner) public view returns (uint256 balance) {
        return balances[_owner];
    }

    function transfer(address _to, uint256 _value) public returns (bool success) {
        require(_to != address(0), "Invalid address");
        require(balances[msg.sender] >= _value, "Insufficient balance");

        balances[msg.sender] -= _value;
        balances[_to] += _value;
        emit Transfer(msg.sender, _to, _value);
        return true;
    }

    function approve(address _spender, uint256 _value) public returns (bool success) {
        allowed[msg.sender][_spender] = _value;
        emit Approval(msg.sender, _spender, _value);
        return true;
    }

    function allowance(address _owner, address _spender) public view returns (uint256 remaining) {
        return allowed[_owner][_spender];
    }

    function transferFrom(address _from, address _to, uint256 _value) public returns (bool success) {
        uint256 _allowance = allowed[_from][msg.sender];
        require(_to != address(0), "Invalid address");
        require(balances[_from] >= _value, "Insufficient balance");
        require(_allowance >= _value, "Allowance exceeded");

        balances[_from] -= _value;
        balances[_to] += _value;
        allowed[_from][msg.sender] -= _value;
        emit Transfer(_from, _to, _value);
        return true;
    }

    /**
     * @dev 水龙头功能：任何人都可以调用，给自己领取 1000 个 mUSD 用于测试
     * （在生产环境中绝对不能有这样的函数）
     */
    function faucet() public {
        uint256 amount = 1000 * (10 ** uint256(decimals));
        totalSupply += amount;
        balances[msg.sender] += amount;
        emit Mint(msg.sender, amount);
        emit Transfer(address(0), msg.sender, amount);
    }

    event Mint(address indexed to, uint256 amount);
}
