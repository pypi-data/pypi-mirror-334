import pandas as pd
from clickhouse_driver import Client
import os
import numpy as np


ch_client = Client(
    host=os.getenv("CLICKHOUSE_HOST", "localhost"),
    port=int(os.getenv("CLICKHOUSE_PORT", "8123")),
    user=os.getenv("CLICKHOUSE_USER", "default"),
    password=os.getenv("CLICKHOUSE_PASSWORD", ""),
    database="us_stocks"
)

# 指標定義
INDICATORS = {
    'rsi_14': {
        'name': 'RSI 14',
        'indicator': 'rsi',
        'description': 'RSI 14',
        'params': {'period': 14},
    },
    'ma_5': {
        'name': 'MA 5',
        'indicator': 'ma',
        'description': 'MA 5',
        'params': {'period': 5},
    },
    'ma_10': {
        'name': 'MA 10',
        'indicator': 'ma',
        'description': 'MA 10',
        'params': {'period': 10},
    },
    'sar': {
        'name': 'SAR',
        'indicator': 'sar',
        'description': 'SAR',
        'params': {},
    },
    'bollinger_bands_upper': {
        'name': 'Bollinger Bands Upper',
        'indicator': 'bollinger_bands_upper',
        'description': 'Bollinger Bands Upper',
        'params': {'period': 20, 'std_dev': 2},
    },
    'bollinger_bands_middle': {
        'name': 'Bollinger Bands Middle',
        'indicator': 'bollinger_bands_middle',
        'description': 'Bollinger Bands Middle',
        'params': {'period': 20, 'std_dev': 2},
    },
    'bollinger_bands_lower': {
        'name': 'Bollinger Bands Lower',
        'indicator': 'bollinger_bands_lower',
        'description': 'Bollinger Bands Lower',
        'params': {'period': 20, 'std_dev': 2},
    },
    'bbi': {
        'name': 'BBI',
        'indicator': 'bbi',
        'description': 'BBI',
        'params': {'period': 10},
    },
    'macd_line': {
        'name': 'MACD Line',
        'indicator': 'macd_line',
        'description': 'MACD Line',
        'params': {'fastperiod': 12, 'slowperiod': 26, 'signalperiod': 9},

    },
    'macd_signal': {
        'name': 'MACD Signal',
        'indicator': 'macd_signal',
        'description': 'MACD Signal',
        'params': {'fastperiod': 12, 'slowperiod': 26, 'signalperiod': 9},
    },
    'macd_histogram': {
        'name': 'MACD Histogram',
        'indicator': 'macd_histogram',
        'description': 'MACD Histogram',
        'params': {'fastperiod': 12, 'slowperiod': 26, 'signalperiod': 9},
    },
    'kdj_k': {
        'name': 'KDJ K',
        'indicator': 'kdj_k',
        'description': 'KDJ K',
        'params': {'period': 9, 'smoothk': 3, 'smoothd': 3},
    },
    'kdj_d': {
        'name': 'KDJ D',
        'indicator': 'kdj_d',
        'description': 'KDJ D',
        'params': {'period': 9, 'smoothk': 3, 'smoothd': 3},
    },
    'kdj_j': {
        'name': 'KDJ J',
        'indicator': 'kdj_j',
        'description': 'KDJ J',
        'params': {'period': 9, 'smoothk': 3, 'smoothd': 3},
    },
    'td_index': {
        'name': 'TD Index',
        'indicator': 'td_index',
        'description': 'TD Index',
        'params': {'period': 9},
    }
}


US_STOCKS_DATABASE = "us_stocks"
US_STOCKS_DAILY_AGGS_TABLE = "daily_aggs"
US_STOCKS_DAILY_SNAPSHOT_TABLE = "daily_snapshot"
US_STOCKS_INDICATORS_TABLE = "indicator_values"


class BullinvQuote:
    @staticmethod
    def get_data(ticker, start_date=None, end_date=None, limit=1000, include_indicators=False):

        # 获取基本的OHLCV数据
        query = f"""SELECT 
            ticker,
            volume,
            open,
            high,
            low,
            close,
            window_start as datetime
        FROM {US_STOCKS_DATABASE}.{US_STOCKS_DAILY_AGGS_TABLE} 
        WHERE ticker = '{ticker}'
        """

        # 添加日期过滤条件
        if start_date:
            query += f" AND window_start >= '{start_date}'"
        if end_date:
            query += f" AND window_start <= '{end_date}'"

        # 添加排序和限制
        query += f" ORDER BY window_start"
        if limit:
            query += f" LIMIT {limit}"

        # 使用with_column_types=True获取列信息
        data, columns = ch_client.execute(query, with_column_types=True)

        # 将data转换为DataFrame
        df = pd.DataFrame(data, columns=[col[0] for col in columns])

        # 转换日期列
        if 'datetime' in df.columns:
            df['datetime'] = pd.to_datetime(df['datetime'])

        # 如果需要包含指标数据
        if include_indicators and not df.empty:

            indicator_query = f"""
            SELECT ticker, date, indicator_id, value
            FROM {US_STOCKS_DATABASE}.{US_STOCKS_INDICATORS_TABLE}
            WHERE ticker = '{ticker}'
            """

            ind_data, ind_columns = ch_client.execute(
                indicator_query, with_column_types=True)

            if ind_data:
                # 创建指标数据框
                ind_df = pd.DataFrame(
                    ind_data, columns=[col[0] for col in ind_columns])

                # 将日期转换为datetime格式
                ind_df['date'] = pd.to_datetime(ind_df['date'])

                # 创建指标数据的透视表
                ind_pivot = ind_df.pivot(
                    index=['ticker', 'date'],
                    columns='indicator_id',
                    values='value'
                ).reset_index()

                # 确保所有指标列都存在
                for ind_id in INDICATORS.keys():
                    if ind_id not in ind_pivot.columns:
                        ind_pivot[ind_id] = np.nan

                # 将OHLCV数据与指标数据合并
                df['date'] = df['datetime'].dt.date
                df['date'] = pd.to_datetime(df['date'])

                # 合并数据
                merged_df = pd.merge(
                    df,
                    ind_pivot,
                    left_on=['ticker', 'date'],
                    right_on=['ticker', 'date'],
                    how='left'
                )

                # 删除临时列
                merged_df = merged_df.drop(columns=['date'])

                df = merged_df

        # sort by datetime
        df = df.sort_values('datetime')
        # reset index
        df = df.reset_index(drop=True)
        return df

    @staticmethod
    def get_screener_date_list() -> pd.DataFrame:
        query = f"""SELECT 
            DISTINCT date
        FROM {US_STOCKS_DATABASE}.{US_STOCKS_DAILY_SNAPSHOT_TABLE}
        ORDER BY date DESC
        """
        data, columns = ch_client.execute(query, with_column_types=True)
        return pd.DataFrame(data, columns=[col[0] for col in columns])
    

    @staticmethod
    def stock_screener(conditions, include_columns: list[str] = ["*"], limit: int = 100) -> pd.DataFrame:
        # 构建完整的查询条件
        where_clauses = []
        join_needed = False

        date_list = BullinvQuote.get_screener_date_list()
        date_list = date_list['date'].tolist()
        t1_date = date_list[0].strftime("%Y-%m-%d")
        t2_date = date_list[1].strftime("%Y-%m-%d")

        if not isinstance(conditions, list):
            conditions = [conditions]

        for condition in conditions:
            if "cross_over" in condition:
                # 解析 cross_over 表达式
                parts = condition.split("cross_over")
                left_indicator = parts[0].strip()
                right_indicator = parts[1].strip()

                # 构建跨天比较的条件，使用最近两个交易日
                where_clauses.append(
                    f"t1.{left_indicator} > t1.{right_indicator} AND t2.{left_indicator} <= t2.{right_indicator}")
                join_needed = True

            elif "cross_under" in condition:
                # 解析 cross_under 表达式
                parts = condition.split("cross_under")
                left_indicator = parts[0].strip()
                right_indicator = parts[1].strip()

                where_clauses.append(
                    f"t1.{left_indicator} < t1.{right_indicator} AND t2.{left_indicator} >= t2.{right_indicator}")
                join_needed = True

            else:
                # 原始条件
                where_clauses.append(condition)

        # 构建查询
        if join_needed:
            columns_str = ",".join(
                [f"t1.{col}" for col in include_columns if col != "*"]) if "*" not in include_columns else "t1.*"
            query = f"""SELECT 
                {columns_str}
            FROM {US_STOCKS_DATABASE}.{US_STOCKS_DAILY_SNAPSHOT_TABLE} AS t1
            LEFT JOIN {US_STOCKS_DATABASE}.{US_STOCKS_DAILY_SNAPSHOT_TABLE} AS t2
            ON t1.ticker = t2.ticker AND t2.date = '{t2_date}'
            WHERE t1.date = '{t1_date}' AND {" AND ".join(where_clauses)}
            LIMIT {limit}
            """
        else:
            columns_str = ",".join(include_columns)
            query = f"""SELECT 
                {columns_str}
            FROM {US_STOCKS_DATABASE}.{US_STOCKS_DAILY_SNAPSHOT_TABLE} 
            WHERE date = '{t1_date}' AND {" AND ".join(where_clauses)}
            LIMIT {limit}
            """

        data, columns = ch_client.execute(query, with_column_types=True)
        # 将data转换为DataFrame
        df = pd.DataFrame(data, columns=[col[0] for col in columns])

        # 检查是否有日期列
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'])
            # 按日期排序
            df = df.sort_values('date')

        # 重置索引
        df = df.reset_index(drop=True)
        return df

    # def gen_filter_func(self,conditions):
    #     # conditions = [
    #     #     {"indicator": "rsi_14", "operator": ">", "value": 50},
    #     #     {"indicator": "volume", "operator": "cross_over", "value": "ma_10"}
    #     # ]
    #     filter_func = ""
    #     for condition in conditions:
    #         if condition["operator"] == "cross_over":
    #             filter_func += f"{condition['indicator']} cross_over {condition['value']} and "
    #         elif condition["operator"] == "cross_under":
    #             filter_func += f"{condition['indicator']} cross_under {condition['value']} and "
