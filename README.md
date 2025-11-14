# trading-analysis

Python 项目模板，用于拉取指定股票在指定时间区间内的走势数据并保存到本地 CSV。

## 环境初始化

1. 创建虚拟环境（可选但推荐）
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
2. 安装依赖
   ```bash
   pip install -r requirements.txt
   ```

> 如果希望以包形式使用，也可以执行 `pip install -e .`。

## 使用方式

### 方式一：安装后直接使用 CLI

```bash
pip install -e .
fetch-stock-data AAPL 2024-01-01 2024-06-30 --interval 1d
```

同等效果的还有 `python -m trading_analysis.cli ...`。

### 方式二：直接运行仓库内脚本（开发模式）

```bash
PYTHONPATH=src python scripts/fetch_stock_data.py AAPL 2024-01-01 2024-06-30 --interval 1d
```

可通过 `-o` 指定输出路径，默认保存在仓库根目录下的 `data/` 中。

### 方式三：在代码中调用

```python
from trading_analysis import fetch_stock_data

fetch_stock_data(
    symbol="MSFT",
    start="2024-01-01",
    end="2024-03-01",
    interval="1d",
)
```

函数将返回 CSV 文件路径，方便后续分析或可视化处理。
