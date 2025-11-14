from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional

import pandas as pd
import yfinance as yf
from dateutil import parser


DEFAULT_DATA_DIR = Path(__file__).resolve().parents[2] / "data"


def _coerce_datetime(value: datetime | str) -> datetime:
    if isinstance(value, datetime):
        return value
    try:
        return parser.isoparse(value)
    except (parser.ParserError, TypeError) as exc:
        raise ValueError(f"无法解析日期: {value}") from exc


@dataclass(slots=True)
class StockDataRequest:
    symbol: str
    start: datetime | str
    end: datetime | str
    interval: str = "1d"
    output_path: Optional[Path] = None

    def normalized_dates(self) -> tuple[datetime, datetime]:
        start_dt = _coerce_datetime(self.start)
        end_dt = _coerce_datetime(self.end)
        if start_dt >= end_dt:
            raise ValueError("结束时间必须晚于开始时间")
        return start_dt, end_dt


def fetch_stock_data(
    request: Optional[StockDataRequest] = None,
    *,
    symbol: Optional[str] = None,
    start: Optional[datetime | str] = None,
    end: Optional[datetime | str] = None,
    interval: str = "1d",
    output_path: Optional[Path | str] = None,
) -> Path:
    """
    下载指定股票在指定时间区间内的历史数据并保存到本地 CSV。

    Parameters
    ----------
    request
        预先构造的 StockDataRequest。
    symbol, start, end, interval, output_path
        当不提供 request 时使用的参数。

    Returns
    -------
    Path
        保存后的 CSV 文件路径。
    """

    if request is None:
        if not all([symbol, start, end]):
            raise ValueError("必须提供 request 或 symbol/start/end 参数")
        resolved_output = Path(output_path) if output_path else None
        request = StockDataRequest(symbol=symbol, start=start, end=end, interval=interval, output_path=resolved_output)

    start_dt, end_dt = request.normalized_dates()
    data = yf.download(
        request.symbol,
        start=start_dt,
        end=end_dt,
        interval=request.interval,
        progress=False,
        auto_adjust=True,
    )

    if data.empty:
        raise ValueError("未获取到任何数据，请检查股票代码或时间区间")

    if not isinstance(data.index, pd.DatetimeIndex):
        data.index = pd.to_datetime(data.index)

    output_path = request.output_path or _default_output_path(request.symbol, start_dt, end_dt, request.interval)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    data.to_csv(output_path)
    return output_path


def _default_output_path(symbol: str, start: datetime, end: datetime, interval: str) -> Path:
    DEFAULT_DATA_DIR.mkdir(parents=True, exist_ok=True)
    start_str = start.strftime("%Y%m%d")
    end_str = end.strftime("%Y%m%d")
    file_name = f"{symbol.replace('.', '_')}_{start_str}_{end_str}_{interval}.csv"
    return DEFAULT_DATA_DIR / file_name
