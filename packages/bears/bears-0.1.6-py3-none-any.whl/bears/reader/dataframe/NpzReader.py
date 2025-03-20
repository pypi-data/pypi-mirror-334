import io
from typing import Dict, List, Optional, Set, Union

import numpy as np

from bears.constants import DataLayout, FileFormat, MLTypeSchema, Storage
from bears.core.frame.ScalableDataFrame import DaskDataFrame, ScalableDataFrame, ScalableDataFrameRawType
from bears.FileMetadata import FileMetadata
from bears.reader.dataframe.DataFrameReader import DataFrameReader
from bears.util import accumulate, as_list, run_concurrent


class NpzReader(DataFrameReader):
    file_formats = [FileFormat.NPZ]
    streams = [io.BytesIO, io.StringIO]

    def _read_npz_to_dict(self, fpath: str, columns: Optional[List[str]], **kwargs) -> Dict:
        npzdata = np.load(fpath, allow_pickle=True)
        if columns is not None:
            return {col: npzdata[col] for col in columns}
        return {col: npzdata[col] for col in npzdata.files}

    def _read_npz_to_dask_df(
        self, source: Union[List[str], str], columns: Optional[List[str]], **kwargs
    ) -> DaskDataFrame:
        npz_dicts_list: List = accumulate(
            [run_concurrent(self._read_npz_to_dict, fpath, columns, **kwargs) for fpath in as_list(source)]
        )
        return ScalableDataFrame.concat(npz_dicts_list, reset_index=True, layout=DataLayout.DASK).dask()

    def _read_raw_sdf(
        self,
        source: Union[str, io.IOBase],
        storage: Storage,
        data_schema: Optional[MLTypeSchema],
        read_as: Optional[DataLayout],
        **kwargs,
    ) -> ScalableDataFrameRawType:
        if storage is Storage.S3:
            raise NotImplementedError(
                "Currently we do not support directly reading .npz files from s3 in NpzReader."
            )
        elif storage is Storage.STREAM:
            raise NotImplementedError(
                "Currently we do not support directly reading from stream in NpzReader."
            )
        return self._read_npz_to_dict(
            source,
            columns=self._filtered_data_columns(source, storage=storage, data_schema=data_schema),
            **(self.filtered_params(np.load)),
        )

    def _read_raw_dask_sdf(
        self,
        source: Union[List[str], str, io.IOBase],
        storage: Storage,
        data_schema: Optional[MLTypeSchema],
        **kwargs,
    ) -> DaskDataFrame:
        import dask.dataframe as dd

        if storage is Storage.STREAM:
            ## Read as another layout and convert to Dask:
            df: ScalableDataFrameRawType = self._read_raw_sdf_with_retries(
                source=source, storage=storage, **kwargs
            )
            return ScalableDataFrame.of(df, layout=DataLayout.DASK, **kwargs).raw()
        else:
            return self._read_npz_to_dask_df(
                source,
                columns=self._filtered_data_columns(source, storage=storage, data_schema=data_schema),
                **self.filtered_params(dd.concat),
            )

    def _filtered_data_columns(
        self,
        source: Union[List[str], str],
        storage: Storage,
        data_schema: Optional[MLTypeSchema],
    ) -> Optional[List[str]]:
        columns: Optional[List[str]] = self._data_columns(data_schema)
        if columns is not None and self.allow_missing_columns and storage is not Storage.STREAM:
            for fpath in as_list(source):
                ## Keep only the common subset of columns...
                file_columns: Optional[List[str]] = self.detect_columns(
                    fpath, storage=storage, raise_error=False
                )
                if file_columns is not None:
                    file_columns: Set[str] = set(file_columns)
                    columns: List[str] = [col for col in columns if col in file_columns]
        return columns

    @classmethod
    def detect_columns(
        cls,
        fpath: str,
        storage: Optional[Storage] = None,
        raise_error: bool = True,
    ) -> Optional[List[str]]:
        if storage is None:
            storage: Storage = FileMetadata.detect_storage(fpath)
        if storage is not Storage.LOCAL_FILE_SYSTEM:
            if raise_error:
                raise ValueError(f"Can only detect columns for npz file on disk, not {storage}")
            return None
        # Without reading the entire file into memory, you can access small fragments of large files
        # on disk by using mmap (https://stackoverflow.com/questions/49219436/)
        npz_file = np.load(fpath, mmap_mode="r", allow_pickle=True)
        return list(npz_file.files)
