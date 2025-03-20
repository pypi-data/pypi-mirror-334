import contextlib
from typing import Any, List

from azure.core.exceptions import (
    ClientAuthenticationError,
    HttpResponseError,
    ResourceExistsError,
    StreamClosedError,
    StreamConsumedError,
    map_error,
)
from azure.core.pipeline import PipelineResponse
from azure.core.tracing.decorator import distributed_trace

from polaris.sdk.project_api._serialization import Serializer

from ...operations._patch import build_upload_file_request
from ._operations import CustomizationsOperations as CustomizationsOperationsGenerated

_SERIALIZER = Serializer()
_SERIALIZER.client_side_validation = False


class CustomizationsOperations(CustomizationsOperationsGenerated):
    @distributed_trace
    async def put_logo(
        self,
        kind: str,
        file: dict[str, tuple[str, bytes]],
        **kwargs: Any,
    ) -> None:
        """Uploads a specified logo for the organization.

        :param kind: The logo type.
        :type kind: str | LogoKind
        :param files: Multipart input for the file to be uploaded.
        :type files: dict[str, tuple[str, bytes]]
        :return: response
        :rtype: Union[LogosResponse, ErrorResponse]
        :raises: ~azure.core.exceptions.HttpResponseError

        Example:
            .. code-block:: python
                with open("logo.png", "rb") as file:
                    data = {"file": ("uniquely_named_file.png", file.read())}
                await self.global_client_async.customizations.put_logo("full", data)
        """
        request = build_upload_file_request(kind, file, **kwargs)
        request.url = self._client.format_url(request.url)

        cls = kwargs.pop("cls", None)
        stream = kwargs.pop("stream", True)
        pipeline_response: PipelineResponse = await self._client._pipeline.run(
            request, stream=stream, **kwargs
        )

        error_map = {
            401: ClientAuthenticationError,
            409: ResourceExistsError,
        }
        error_map.update(kwargs.pop("error_map", {}) or {})
        response = pipeline_response.http_response

        with contextlib.suppress(StreamConsumedError, StreamClosedError):
            response.read()  # Load the body in memory and close the socket

        if response.status_code not in [200, 400, 404]:
            map_error(
                status_code=response.status_code, response=response, error_map=error_map
            )
            raise HttpResponseError(response=response)

        if response.status_code in [200]:
            deserialized = self._deserialize("LogosResponse", response)

        if response.status_code in [400, 404]:
            deserialized = self._deserialize("ErrorResponse", response)

        if cls:
            return cls(pipeline_response, deserialized, {})
        return deserialized


__all__: List[str] = ["CustomizationsOperations"]


def patch_sdk():
    """Do not remove from this file.

    `patch_sdk` is a last resort escape hatch that allows you to do customizations
    you can't accomplish using the techniques described in
    https://aka.ms/azsdk/python/dpcodegen/python/customize
    """
