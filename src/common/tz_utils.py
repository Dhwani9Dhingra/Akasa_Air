import pandas as pd
import pytz
from src.common.config import settings

def to_utc(df: pd.DataFrame, col: str = "order_date_time") -> pd.DataFrame:
    src_tz = pytz.timezone(settings.SOURCE_TZ)
    df[col] = pd.to_datetime(df[col])
    df[col + "_utc"] = (
        df[col]
        .dt.tz_localize(src_tz)
        .dt.tz_convert(pytz.utc)
    )
    return df
