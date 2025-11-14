from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path

from .data_fetcher import fetch_stock_data


def _valid_date(value: str) -> str:
    try:
        datetime.fromisoformat(value)
        return value
    except ValueError as exc:
        msg = "日期格式需符合 ISO 8601，例如 2024-01-01 或 2024-01-01T09:30:00"
        raise argparse.ArgumentTypeError(msg) from exc


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="下载指定股票在指定时间区间内的走势数据并保存为 CSV 文件")
    parser.add_argument("symbol", help="股票代码，例如 AAPL、MSFT、000001.SZ 等")
    parser.add_argument("start", type=_valid_date, help="开始时间（含），ISO 8601 格式")
    parser.add_argument("end", type=_valid_date, help="结束时间（不含），ISO 8601 格式")
    parser.add_argument("--interval", default="1d", help="采样间隔，默认 1d，可选 1m/5m/1h/1d/1wk/1mo 等")
    parser.add_argument("-o", "--output", type=Path, help="CSV 输出路径，默认保存在仓库 data 目录")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    output_path = fetch_stock_data(
        symbol=args.symbol,
        start=args.start,
        end=args.end,
        interval=args.interval,
        output_path=args.output,
    )
    print(f"已保存到 {output_path}")
