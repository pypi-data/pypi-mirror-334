import contextlib
from typing import Any, List, Optional, Union

from azure.core.exceptions import (
    ClientAuthenticationError,
    HttpResponseError,
    ResourceExistsError,
    ResourceNotFoundError,
    StreamClosedError,
    StreamConsumedError,
    map_error,
)
from azure.core.pipeline import PipelineResponse
from azure.core.tracing.decorator import distributed_trace

from polaris.sdk.project_api._serialization import Serializer
from polaris.sdk.project_api.models._enums import CompressionFormat, DataFormat
from polaris.sdk.project_api.models._models import ErrorResponse, FileMetadata

from ...operations._patch import build_upload_file_request
from ._operations import FilesOperations as FilesOperationsGenerated

_SERIALIZER = Serializer()
_SERIALIZER.client_side_validation = False


class FilesOperations(FilesOperationsGenerated):
    @distributed_trace
    async def upload_file(
        self,
        files: dict[str, tuple[str, bytes]],
        *,
        data_format: Optional[DataFormat] = None,
        compression_format: Optional[CompressionFormat] = None,
        **kwargs: Any,
    ) -> Union[FileMetadata, ErrorResponse]:
        """Uploads a file to the Polaris staging area.

        :param files: Multipart input for the file to be uploaded.
        :type files: dict[str, any]
        :param data_format: If specified, the format of the data.
        Otherwise, Polaris infers the data format from the filename or Content-Type.
        :type data_format: dict[str, any]
        :param compression_format: If specified, the compression used for the file.
            Otherwise, Polaris infers the compression from the filename or Content-Type.
        :type compression_format: dict[str, any]
        :return: response
        :rtype: Union[FileMetadata, ErrorResponse]
        :raises: ~azure.core.exceptions.HttpResponseError

        Example:
            .. code-block:: python
                with open("input.json", "rb") as file:
                    data = {"file": ("uniquely_named_file.json", file.read())}
                await self.client_async.project_files.upload_file(data)
        """
        request = build_upload_file_request(
            self._config.project_id, files, data_format, compression_format, **kwargs
        )
        request.url = self._client.format_url(request.url)

        cls = kwargs.pop("cls", None)
        stream = kwargs.pop("stream", True)
        pipeline_response: PipelineResponse = await self._client._pipeline.run(
            request, stream=stream, **kwargs
        )

        error_map = {
            401: ClientAuthenticationError,
            404: ResourceNotFoundError,
            409: ResourceExistsError,
        }
        error_map.update(kwargs.pop("error_map", {}) or {})
        response = pipeline_response.http_response

        with contextlib.suppress(StreamConsumedError, StreamClosedError):
            response.read()  # Load the body in memory and close the socket

        if response.status_code not in [200, 201, 400, 500]:
            map_error(
                status_code=response.status_code, response=response, error_map=error_map
            )
            raise HttpResponseError(response=response)

        if response.status_code in [200, 201]:
            deserialized = self._deserialize("FileMetadata", response)

        if response.status_code in [400, 500]:
            deserialized = self._deserialize("ErrorResponse", response)

        if cls:
            return cls(pipeline_response, deserialized, {})
        return deserialized


__all__: List[str] = ["FilesOperations"]


def patch_sdk():
    """Do not remove from this file.

    `patch_sdk` is a last resort escape hatch that allows you to do customizations
    you can't accomplish using the techniques described in
    https://aka.ms/azsdk/python/dpcodegen/python/customize
    """
