# trading-analysis

Python 项目模板，用于拉取指定股票在指定时间区间内的走势数据并保存到本地 CSV。

## 环境初始化（使用 uv）

1. 安装 uv（一次性操作）
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   source $HOME/.local/bin/env
   ```
2. 同步依赖并创建虚拟环境
   ```bash
   uv sync
   ```
   命令会在项目根目录生成 `.venv/`，并以可编辑模式安装当前包。

> 如果确实需要使用 pip，可手动执行 `python3 -m venv .venv && source .venv/bin/activate && pip install -e .`.

## 使用方式

### 方式一：使用 uv 暴露的 CLI

```bash
uv run fetch-stock-data AAPL 2024-01-01 2024-06-30 --interval 1d
```

同样可以使用 `uv run python -m trading_analysis.cli ...`。

### 方式二：直接运行仓库脚本（开发模式）

```bash
uv run python scripts/fetch_stock_data.py AAPL 2024-01-01 2024-06-30 --interval 1d
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
