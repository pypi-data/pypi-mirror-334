from typing import Any, List, Optional, Union

import numpy as np
import pandas as pd

from bears.constants import DataLayout
from bears.core.frame.ScalableDataFrame import ScalableDataFrame
from bears.core.frame.ScalableSeries import SS_DEFAULT_NAME, ScalableSeries
from bears.util import get_default, is_function, wrap_fn_output


class PandasScalableSeries(ScalableSeries):
    layout = DataLayout.PANDAS
    layout_validator = ScalableSeries.is_pandas

    def __init__(self, data: Union[pd.Series, ScalableSeries], name: Optional[str] = None, **kwargs):
        super(self.__class__, self).__init__(**kwargs)
        if isinstance(data, ScalableSeries):
            data: pd.Series = data.pandas(**kwargs)
        self.layout_validator(data)
        self._data: pd.Series = data
        if name is not None and not isinstance(name, (str, int, float)):
            raise ValueError(
                f"`name` used to construct {self.__class__} can only be int, str or float; "
                f"found object of type: {type(name)} with value: {name}"
            )
        else:
            self._data.name = name
        self._name: Optional[str] = name

    def __len__(self):
        return len(self._data)

    def __str__(self):
        name_str: str = "" if self._name is None else f'"{self._name}": '
        out = f"{name_str}Pandas Series of dtype `{self._data.dtype}` with {len(self)} items:\n"
        # out += '\n' + '-' * len(out) + '\n'
        out += str(self._data)
        return out

    @classmethod
    def _to_scalable(cls, data: Any) -> Union[ScalableSeries, ScalableDataFrame, Any]:
        if isinstance(data, np.ndarray):
            return ScalableSeries.get_subclass(DataLayout.NUMPY)(data)
        if isinstance(data, pd.Series):
            return ScalableSeries.get_subclass(DataLayout.PANDAS)(data)
        if isinstance(data, pd.DataFrame):
            return ScalableDataFrame.get_subclass(DataLayout.PANDAS)(data)
        return data

    def __getattr__(self, attr_name: str):
        """Forwards calls to the respective method of Pandas Series class."""
        out = super().__getattr__(attr_name)
        if is_function(out):
            return wrap_fn_output(out, wrapper_fn=self._to_scalable)
        return self._to_scalable(out)

    def __getitem__(self, key: Any):
        return self._to_scalable(self._data[key])

    def __setitem__(self, key: Any, value: Any):
        # self._data[key] = value
        raise NotImplementedError("Cannot set at the moment")

    def as_list(self, **kwargs) -> List:
        return list(self._data.tolist())

    def as_pandas(self, **kwargs) -> pd.Series:
        return self._data

    def _to_frame_raw(self, **kwargs):
        kwargs["name"]: Any = get_default(self._name, SS_DEFAULT_NAME)
        return self._data.to_frame(**kwargs)
