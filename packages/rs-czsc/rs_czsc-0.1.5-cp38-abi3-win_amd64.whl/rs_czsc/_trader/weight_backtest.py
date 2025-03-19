import pandas as pd
from rs_czsc._rs_czsc import PyWeightBacktest, daily_performance
from rs_czsc._utils._df_convert import arrow_bytes_to_pd_df, pandas_to_arrow_bytes


class WeightBacktest:
    """持仓权重回测

    飞书文档：https://s0cqcxuy3p.feishu.cn/wiki/Pf1fw1woQi4iJikbKJmcYToznxb
    """

    def __init__(
        self,
        dfw: pd.DataFrame,
        digits: int = 2,
        fee_rate: float = 0.0002,
        n_jobs: int = 1,
        weight_type: str = "ts",
        yearly_days: int = 252,
    ) -> None:
        """持仓权重回测

        初始化函数逻辑：

        1. 将传入的kwargs保存在实例变量self.kwargs中。
        2. 复制传入的dfw到实例变量self.dfw。
        3. 检查self.dfw中是否存在空值，如果存在则抛出ValueError异常，并提示"dfw 中存在空值，请先处理"。
        4. 设置实例变量self.digits为传入的digits值。
        5. 从kwargs中获取'fee_rate'参数的值，默认为0.0002，并将其保存在实例变量self.fee_rate中。
        6. 将self.dfw中的 weight 列转换为浮点型，并保留self.digits位小数。
        7. 提取self.dfw中的唯一交易标的符号，并将其保存在实例变量self.symbols中。
        8. 执行backtest()方法进行回测，并将结果保存在实例变量self.results中。

        :param dfw: pd.DataFrame, columns = ['dt', 'symbol', 'weight', 'price'], 持仓权重数据，其中

            dt      为K线结束时间，必须是连续的交易时间序列，不允许有时间断层
            symbol  为合约代码，
            weight  为K线结束时间对应的持仓权重，品种之间的权重是独立的，不会互相影响
            price   为结束时间对应的交易价格，可以是当前K线的收盘价，或者下一根K线的开盘价，或者未来N根K线的TWAP、VWAP等

            数据样例如下：
            ===================  ========  ========  =======
            dt                   symbol      weight    price
            ===================  ========  ========  =======
            2019-01-02 09:01:00  DLi9001       0.5   961.695
            2019-01-02 09:02:00  DLi9001       0.25  960.72
            2019-01-02 09:03:00  DLi9001       0.25  962.669
            2019-01-02 09:04:00  DLi9001       0.25  960.72
            2019-01-02 09:05:00  DLi9001       0.25  961.695
            ===================  ========  ========  =======

        :param digits: int, 权重列保留小数位数
        :param weight_type: str, default 'ts'，持仓权重类别，可选值包括：'ts'、'cs'，分别表示时序策略、截面策略
        :param yearly_days: int, default 252，年化交易日数量
        :param fee_rate: float, default 0.0002，单边交易成本，包括手续费与冲击成本
        :param n_jobs: int, default 4，并行计算的进程数
        """
        if dfw['weight'].dtype != 'float':
            dfw['weight'] = dfw['weight'].astype(float)
        if dfw.isnull().sum().sum() > 0:
            raise ValueError(f"dfw 中存在空值，请先处理; 具体数据：\n{dfw[dfw.isnull().T.any().T]}")

        data = pandas_to_arrow_bytes(dfw)
        self._inner: PyWeightBacktest = PyWeightBacktest.from_arrow(
            data,
            digits,
            fee_rate,
            n_jobs,
            weight_type,
            yearly_days,
        )
        self.weight_type = weight_type
        self.yearly_days = yearly_days

    @property
    def stats(self) -> dict:
        """回测绩效评价"""
        return self._inner.stats()

    @property
    def daily_return(self) -> pd.DataFrame:
        """品种等权费后日收益率"""
        return arrow_bytes_to_pd_df(self._inner.daily_return())

    @property
    def dailys(self) -> pd.DataFrame:
        """品种每日的交易信息

        columns = ['date', 'symbol', 'edge', 'return', 'cost', 'n1b', 'turnover']

        其中:
            date        交易日，
            symbol      合约代码，
            n1b         品种每日收益率，
            edge        策略每日收益率，
            return      策略每日收益率减去交易成本后的真实收益，
            cost        交易成本
            turnover    当日的单边换手率
        """
        return arrow_bytes_to_pd_df(self._inner.dailys())

    @property
    def alpha(self) -> pd.DataFrame:
        """策略超额收益

        columns = ['date', '策略', '基准', '超额']
        """
        return arrow_bytes_to_pd_df(self._inner.alpha())

    @property
    def alpha_stats(self) -> dict:
        """策略超额收益统计"""
        alpha_df = self.alpha
        stats = daily_performance(alpha_df["超额"].to_list(), yearly_days=self.yearly_days)
        stats["开始日期"] = alpha_df["date"].min().strftime("%Y-%m-%d")
        stats["结束日期"] = alpha_df["date"].max().strftime("%Y-%m-%d")
        return stats

    @property
    def bench_stats(self) -> dict:
        """基准收益统计"""
        alpha_df = self.alpha
        stats = daily_performance(alpha_df["基准"].to_list(), yearly_days=self.yearly_days)
        stats["开始日期"] = alpha_df["date"].min().strftime("%Y-%m-%d")
        stats["结束日期"] = alpha_df["date"].max().strftime("%Y-%m-%d")
        return stats

    @property
    def long_daily_return(self):
        """多头每日收益率"""
        df = self.dailys.copy()
        dfv = pd.pivot_table(df, index="date", columns="symbol", values="long_return").fillna(0)

        if self.weight_type == "ts":
            dfv["total"] = dfv.mean(axis=1)
        elif self.weight_type == "cs":
            dfv["total"] = dfv.sum(axis=1)
        else:
            raise ValueError(f"weight_type {self.weight_type} not supported")

        dfv = dfv.reset_index(drop=False)
        return dfv

    @property
    def short_daily_return(self):
        """空头每日收益率"""
        df = self.dailys.copy()
        dfv = pd.pivot_table(df, index="date", columns="symbol", values="short_return").fillna(0)

        if self.weight_type == "ts":
            dfv["total"] = dfv.mean(axis=1)
        elif self.weight_type == "cs":
            dfv["total"] = dfv.sum(axis=1)
        else:
            raise ValueError(f"weight_type {self.weight_type} not supported")

        dfv = dfv.reset_index(drop=False)
        return dfv

    @property
    def long_stats(self):
        """多头收益统计"""
        df = self.long_daily_return.copy()
        stats = daily_performance(df["total"].to_list(), yearly_days=self.yearly_days)
        stats["开始日期"] = df["date"].min().strftime("%Y-%m-%d")
        stats["结束日期"] = df["date"].max().strftime("%Y-%m-%d")
        return stats

    @property
    def short_stats(self):
        """空头收益统计"""
        df = self.short_daily_return.copy()
        stats = daily_performance(df["total"].to_list(), yearly_days=self.yearly_days)
        stats["开始日期"] = df["date"].min().strftime("%Y-%m-%d")
        stats["结束日期"] = df["date"].max().strftime("%Y-%m-%d")
        return stats
