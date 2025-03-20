import pandas as pd
import numpy as np
from dataclasses import dataclass
from sklearn.base import BaseEstimator, TransformerMixin

from .time_validator import TimeValidator
from .tte import Tte

@dataclass
class GroupAggregate(BaseEstimator, TransformerMixin, TimeValidator):
    """
    Трансформер для расчета индивидуальной фичи с помощью переданного 
    трансформера (например, Tte) и добавления агрегированного признака,
    рассчитанного по всем предыдущим наблюдениям.
    
    Parameters
    ----------
    id_col: str = "object_id"
        Колонка с идентификатором объекта.
    time_col: str = "time"
        Колонка с временными метками.
    individual_transformer: BaseEstimator, по умолчанию Tte.
        Трансформер для расчета индивидуальной фичи.
    feature_col: str = "tte"
        Имя вычисленной индивидуальной фичи.
    agg_func: str = "mean"
        Функция агрегации (на данный момент поддерживается "mean").
    
    Returns
    -------
    pd.DataFrame: Датафрейм с исходной индивидуальной фичей и 
                  агрегированным признаком.
    
    Example
    -------
    >>> import pandas as pd
    >>> from datetime import datetime
    >>> df = pd.DataFrame({
    ...     "object_id": [1, 2, 1, 2],
    ...     "time": [
    ...         datetime(2025, 1, 1, 9, 10),
    ...         datetime(2025, 1, 1, 10, 11),
    ...         datetime(2025, 1, 2, 9, 10),
    ...         datetime(2025, 1, 3, 10, 11)
    ...     ],
    ... })
    >>> result = GroupAggregate().transform(df)
    >>> print(result.to_string(index=False))
     object_id                time  tte  agg_tte
             1 2025-01-01 09:10:00  1.0      NaN
             2 2025-01-01 10:11:00  2.0      1.0
             1 2025-01-02 09:10:00  NaN      1.5
             2 2025-01-03 10:11:00  NaN      1.5
    """

    id_col: str = "object_id"
    time_col: str = "time"
    individual_transformer: BaseEstimator = None
    feature_col: str = "tte"
    agg_func: str = "mean"

    def __post_init__(self):
        if self.individual_transformer is None:
            self.individual_transformer = Tte(
                time_col=self.time_col, tte_col=self.feature_col)
            
    def fit(self, X: pd.DataFrame, y=None):
        required_cols = {self.id_col, self.time_col}
        if not required_cols.issubset(X.columns):
            raise ValueError(
                f"В данных отсутствуют необходимые колонки: "
                f"{required_cols}"
            )
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        self._validate_time_column(X)
        
        individual_results = []
        for _, df_ind in X.groupby(self.id_col):
            df_copy = df_ind.copy()
            df_transformed = self.individual_transformer.transform(df_copy)
            individual_results.append(df_transformed)
        enriched_df = pd.concat(individual_results, ignore_index=True)
        
        enriched_df = enriched_df.sort_values(self.time_col) \
            .reset_index(drop=True)
        
        if self.agg_func == "mean":
            cum_agg = enriched_df[self.feature_col].expanding(min_periods=1) \
            .apply(lambda x: np.nanmean(x), raw=False)
        else:
            cum_agg = enriched_df[self.feature_col].expanding(min_periods=1) \
                .agg(self.agg_func)
        
        enriched_df[f"agg_{self.feature_col}"] = cum_agg.shift(1)
        
        return enriched_df
