"""
SolarMRV 测试配置文件
- 提供测试公共 fixture
- 自动把项目根目录加入 sys.path，便于直接 import 顶层模块
"""
import os
import sys
from pathlib import Path

# 把项目根目录加入 sys.path
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import pytest


@pytest.fixture(scope="session")
def project_root():
    """返回项目根目录绝对路径"""
    return ROOT


@pytest.fixture(scope="session")
def data_dir(project_root):
    """采集数据目录"""
    return project_root / "data"


@pytest.fixture(scope="function")
def temp_csv(tmp_path):
    """为测试提供临时 CSV 路径"""
    return tmp_path / "test_solar_data.csv"


@pytest.fixture(scope="session")
def sm2_test_keypair():
    """提供测试用 SM2 密钥对（不要用于生产）"""
    return {
        "private_key": "00" + "11" * 32,
        "public_key": "22" * 64,
    }
