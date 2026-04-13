from __future__ import annotations
from collections.abc import Callable
from kiota_abstractions.base_request_builder import BaseRequestBuilder
from kiota_abstractions.get_path_parameters import get_path_parameters
from kiota_abstractions.request_adapter import RequestAdapter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .send_messages.send_messages_request_builder import SendMessagesRequestBuilder

class RsRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /gw/rs
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, dict[str, Any]]) -> None:
        """
        Instantiates a new RsRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/gw/rs", path_parameters)
    
    @property
    def send_messages(self) -> SendMessagesRequestBuilder:
        """
        The sendMessages property
        """
        from .send_messages.send_messages_request_builder import SendMessagesRequestBuilder

        return SendMessagesRequestBuilder(self.request_adapter, self.path_parameters)
    

