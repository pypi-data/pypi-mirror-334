import io
import pickle
from typing import List, Optional, Union

from bears.constants import FileContents, FileFormat, MLTypeSchema
from bears.reader.Reader import Reader
from bears.util import FileSystemUtil, String, StructuredBlob, safe_validate_arguments
from bears.util.aws import S3Util
from bears.util.language import is_list_like


class PickleReader(Reader):
    file_contents = [
        FileContents.PICKLED_OBJECT,
    ]
    streams = [io.BytesIO]
    file_formats = [FileFormat.PICKLE]

    @safe_validate_arguments
    def _read_stream(
        self,
        stream: io.BytesIO,
        file_contents: Optional[FileContents] = None,
        data_schema: Optional[MLTypeSchema] = None,
        **kwargs,
    ) -> StructuredBlob:
        error_to_raise: Optional[Exception] = None
        for _ in range(self.retry):
            try:
                stream.seek(0)
                return pickle.load(stream)
            except Exception as e:
                error_to_raise = e
        raise error_to_raise

    @safe_validate_arguments
    def _read_url(
        self,
        url: Union[str, List[str]],
        file_contents: Optional[FileContents] = None,
        data_schema: Optional[MLTypeSchema] = None,
        **kwargs,
    ) -> StructuredBlob:
        raise NotImplementedError()

    @safe_validate_arguments
    def _read_local(
        self,
        local_path: Union[str, List[str]],
        file_contents: Optional[FileContents] = None,
        data_schema: Optional[MLTypeSchema] = None,
        **kwargs,
    ) -> StructuredBlob:
        error_to_raise: Optional[Exception] = None
        for _ in range(self.retry):
            try:
                if is_list_like(local_path):
                    if len(local_path) > 1:
                        raise IOError(f'More than one pickle file found:\n"{local_path}"')
                    local_path: str = local_path[0]
                return FileSystemUtil.get_file_pickle(
                    local_path,
                )
            except Exception as e:
                error_to_raise = e
        raise error_to_raise

    @safe_validate_arguments
    def _read_s3(
        self,
        s3_path: Union[str, List[str]],
        file_contents: Optional[FileContents] = None,
        data_schema: Optional[MLTypeSchema] = None,
        files_to_ignore: List[str] = String.FILES_TO_IGNORE,
        **kwargs,
    ) -> StructuredBlob:
        error_to_raise: Optional[Exception] = None
        for _ in range(self.retry):
            try:
                if is_list_like(s3_path):
                    if len(s3_path) > 1:
                        raise IOError(f'More than one config file found:\n"{s3_path}"')
                    s3_path: str = s3_path[0]
                return S3Util.get_s3_object_pickle(
                    s3_path,
                )
            except Exception as e:
                error_to_raise = e
        raise error_to_raise
