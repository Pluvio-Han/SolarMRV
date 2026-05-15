// ============================================================================
// DEPRECATED 2026-02：本合约属于项目早期原型阶段产物。结合 2026 年初监管环境变化（参见
// 八部门关于现实世界资产代币化业务的政策口径），项目已主动剥离全部金融化属性。本文件不再
// 部署、不再调用，仅作为早期技术原型阶段的代码留痕。
// 当前在用合约：contracts/SolarDataStore.sol（纯数据存证，不涉及任何价值转移逻辑）。
// 当前项目定位：分布式光伏 MRV（监测—报告—核查）可信数据底座。
// ============================================================================

pragma solidity ^0.4.25;

/**
 * @title StandardERC20
 * @dev 基本的ERC20代币实现 (适用 FISCO-BCOS 0.4.25)
 */
contract StandardERC20 {
    string public name;
    string public symbol;
    uint8 public decimals;
    uint256 public totalSupply;

    mapping(address => uint256) public balances;
    mapping(address => mapping(address => uint256)) public allowed;

    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);

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
}

/**
 * @title SolarToken (SLG)
 * @dev 太阳能绿电积分代币
 * 具有 Minter 角色，仅允许授权的智能合约（预言机/SolarRWA合约）来造币
 */
contract SolarToken is StandardERC20 {
    address public owner;
    
    // 允许铸币的白名单（比如 SolarRWA 核心合约地址）
    mapping(address => bool) public minters;

    event MinterAdded(address indexed account);
    event MinterRemoved(address indexed account);
    event Mint(address indexed to, uint256 amount);

    constructor() public {
        name = "Solar Green Token";
        symbol = "SLG";
        decimals = 18;
        totalSupply = 0;
        owner = msg.sender;
        
        // 部署者默认是第一个 minter
        minters[msg.sender] = true;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner can call this");
        _;
    }

    modifier onlyMinter() {
        require(minters[msg.sender], "Caller is not a minter");
        _;
    }

    function addMinter(address account) public onlyOwner {
        minters[account] = true;
        emit MinterAdded(account);
    }

    function removeMinter(address account) public onlyOwner {
        minters[account] = false;
        emit MinterRemoved(account);
    }

    /**
     * @dev 只有 Minter 才能调用此方法，凭空增发代币
     */
    function mint(address _to, uint256 _amount) public onlyMinter returns (bool) {
        require(_to != address(0), "Mint to zero address");
        totalSupply += _amount;
        balances[_to] += _amount;
        emit Mint(_to, _amount);
        emit Transfer(address(0), _to, _amount);
        return true;
    }
}
