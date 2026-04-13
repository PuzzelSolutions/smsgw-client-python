from __future__ import annotations
from collections.abc import Callable
from kiota_abstractions.base_request_builder import BaseRequestBuilder
from kiota_abstractions.get_path_parameters import get_path_parameters
from kiota_abstractions.request_adapter import RequestAdapter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .batch.batch_request_builder import BatchRequestBuilder

class WithServiceItemRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /management/{serviceId}
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, dict[str, Any]]) -> None:
        """
        Instantiates a new WithServiceItemRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/management/{serviceId}", path_parameters)
    
    @property
    def batch(self) -> BatchRequestBuilder:
        """
        The batch property
        """
        from .batch.batch_request_builder import BatchRequestBuilder

        return BatchRequestBuilder(self.request_adapter, self.path_parameters)
    

