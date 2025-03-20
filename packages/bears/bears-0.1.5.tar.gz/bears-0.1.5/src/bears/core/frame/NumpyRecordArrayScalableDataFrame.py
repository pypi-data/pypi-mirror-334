from typing import Any, Dict, List, Optional, Set, Tuple, Union

import numpy as np
import pandas as pd
from pydantic import conint

from bears.constants import DataLayout
from bears.core.frame.NumpyArrayScalableSeries import NumpyArrayScalableSeries
from bears.core.frame.ScalableDataFrame import ScalableDataFrame, ScalableDataFrameRawType
from bears.util import String, filter_kwargs, safe_validate_arguments

NumpyRecordArrayScalableDataFrame = "NumpyRecordArrayScalableDataFrame"


class NumpyRecordArrayScalableDataFrame(ScalableDataFrame):
    layout = DataLayout.NUMPY_RECORD_ARRAY
    layout_validator = ScalableDataFrame.is_numpy_record_array
    ScalableSeriesClass = NumpyArrayScalableSeries

    def __init__(self, data: Union[np.recarray, ScalableDataFrame], name: Optional[str] = None, **kwargs):
        super(self.__class__, self).__init__(**kwargs)
        if isinstance(data, ScalableDataFrame):
            data: np.recarray = data.numpy(**kwargs)
        self.layout_validator(data)
        self._data: np.recarray = data
        if name is not None and not isinstance(name, (str, int, float)):
            raise ValueError(
                f"`name` used to construct {self.__class__} can only be int, str or float; "
                f"found object of type: {type(name)} with value: {name}"
            )
        self._name: Optional[str] = name

    @property
    def shape(self) -> Tuple[int, int]:
        return self._data.shape

    @property
    def columns(self) -> List:
        return sorted(list(self._data.dtype.names))

    @property
    def columns_set(self) -> Set:
        return set(self._data.dtype.names)

    def __len__(self):
        return self._data.shape[0]

    def __str__(self):
        name_str: str = "" if self._name is None else f'"{self._name}": '
        columns: List = self.columns
        out = f"{name_str}NumPy Record Array of {len(self)} rows with {len(columns)} column(s)."
        width = len(out)
        out += "\n" + "-" * width + "\n"
        out += f"Columns: {columns}"
        out += "\n" + "-" * width + "\n"
        if len(self._data) == 0:
            data_sample = str([])
        elif len(self._data) == 1:
            data_sample = String.pretty(self._data[0])
        elif len(self._data) == 2:
            data_sample = f"{String.pretty(self._data[0])}\n{String.pretty(self._data[1])}"
        else:
            data_sample = f"{String.pretty(self._data[0])}\n...\n{String.pretty(self._data[-1])}"
        out += data_sample
        return out

    def _repr_html_(self):
        name_str: str = "" if self._name is None else f'"{self._name}": '
        columns: List = self.columns
        out = f"<b>{name_str}NumPy Record Array of <code>{len(self)}</code> rows with <code>{len(columns)}</code> column(s)</b>"
        out += "<hr>"
        out += f"<b>Columns:</b><pre>{columns}</pre>"
        out += "<hr><b>Data:</b>"
        if len(self._data) == 0:
            data_sample = ""
        elif len(self._data) == 1:
            data_sample = f"<pre>{String.pretty(self._data[0])}</pre>"
        elif len(self._data) == 2:
            data_sample = f"<pre>{String.pretty(self._data[0])}\n{String.pretty(self._data[1])}</pre>"
        else:
            data_sample = f"<pre>{String.pretty(self._data[0])}\n...\n{String.pretty(self._data[-1])}</pre>"
        out += f"{data_sample}"
        return f"<div>{out}</div>"

    def _repr_latex_(self):
        return self._repr_html_()

    def __getitem__(self, key: Any) -> pd.Series:
        return self._data[key]

    def __setitem__(self, key: Any, value: pd.Series):
        self._data[key] = value

    def _sorted_items_dict(self) -> Dict[str, NumpyArrayScalableSeries]:
        return {col: self.ScalableSeriesClass(self._data[col], name=col) for col in sorted(self.columns)}

    @property
    def loc(self) -> Any:
        return self

    def apply(self, func, axis=1, args=(), **kwargs):
        return self._data.apply(func, axis=axis, raw=False, result_type=None, args=args, **kwargs)

    @classmethod
    def _concat_sdfs(
        cls, dfs: List[ScalableDataFrame], reset_index: bool
    ) -> NumpyRecordArrayScalableDataFrame:
        df_list: List[pd.DataFrame] = []
        for df in dfs:
            assert isinstance(df, cls)
            df_list.append(df._data)
        return cls.of(pd.concat(df_list), layout=cls.layout)

    def as_dict(self, **kwargs) -> Dict:
        return {col: self._data[col] for col in self.columns}

    def as_list_of_dict(self, **kwargs) -> List[Dict]:
        cols = self.columns
        return [dict(zip(cols, d)) for d in self._data]

    def as_numpy(self, **kwargs) -> np.recarray:
        return self._data

    def as_pandas(self, **kwargs) -> pd.DataFrame:
        return pd.DataFrame(self._data, **filter_kwargs(pd.DataFrame.__init__, **kwargs))

    @safe_validate_arguments
    def _stream_chunks(
        self,
        num_rows: Optional[conint(ge=1)] = None,
        num_chunks: Optional[conint(ge=1)] = None,
        stream_as: Optional[DataLayout] = None,
        raw: bool = False,
        shuffle: bool = False,
        seed: Optional[int] = None,
        shard: Tuple[conint(ge=0), conint(ge=1)] = (0, 1),
        reverse_sharding: bool = False,
        drop_last: Optional[bool] = None,
        **kwargs,
    ) -> Union[ScalableDataFrame, ScalableDataFrameRawType]:
        df: np.recarray = self._data
        if shuffle:
            df: pd.DataFrame = df.sample(frac=1, random_state=seed)
        if num_rows is None:
            num_rows = len(df)  ## Return a single chunk
        for i in range(0, len(df), num_rows):
            ## Convert to the respective data layout, then select chunks.
            ## This is done because selecting small chunks is faster as a list of dicts.
            df_chunk = ScalableDataFrame.of(df, layout=stream_as)
            df_chunk = ScalableDataFrame.of(df_chunk.iloc[i : i + num_rows], layout=stream_as)
            if raw:
                yield df_chunk.raw()
            else:
                yield df_chunk
