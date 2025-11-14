"""
trading_analysis
~~~~~~~~~~~~~~~~

提供用于下载指定股票在指定时间区间内走势数据的工具。
"""

from .data_fetcher import fetch_stock_data, StockDataRequest

__all__ = ["fetch_stock_data", "StockDataRequest"]
