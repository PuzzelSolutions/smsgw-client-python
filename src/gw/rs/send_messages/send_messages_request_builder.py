from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.base_request_builder import BaseRequestBuilder
from kiota_abstractions.base_request_configuration import RequestConfiguration
from kiota_abstractions.default_query_parameters import QueryParameters
from kiota_abstractions.get_path_parameters import get_path_parameters
from kiota_abstractions.method import Method
from kiota_abstractions.request_adapter import RequestAdapter
from kiota_abstractions.request_information import RequestInformation
from kiota_abstractions.request_option import RequestOption
from kiota_abstractions.serialization import Parsable, ParsableFactory
from typing import Any, Optional, TYPE_CHECKING, Union
from warnings import warn

if TYPE_CHECKING:
    from ....models.gateway_request import GatewayRequest
    from ....models.gateway_response import GatewayResponse
    from ....models.problem_details import ProblemDetails

class SendMessagesRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /gw/rs/sendMessages
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, dict[str, Any]]) -> None:
        """
        Instantiates a new SendMessagesRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/gw/rs/sendMessages?Message={Message}&Password={Password}&Username={Username}{&BatchReference*,ServiceId*}", path_parameters)
    
    async def get(self,request_configuration: Optional[RequestConfiguration[SendMessagesRequestBuilderGetQueryParameters]] = None) -> Optional[bytes]:
        """
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: bytes
        """
        request_info = self.to_get_request_information(
            request_configuration
        )
        if not self.request_adapter:
            raise Exception("Http core is null") 
        return await self.request_adapter.send_primitive_async(request_info, "bytes", None)
    
    async def post(self,body: GatewayRequest, request_configuration: Optional[RequestConfiguration[QueryParameters]] = None) -> Optional[GatewayResponse]:
        """
        param body: The request body
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[GatewayResponse]
        """
        if body is None:
            raise TypeError("body cannot be null.")
        request_info = self.to_post_request_information(
            body, request_configuration
        )
        from ....models.problem_details import ProblemDetails

        error_mapping: dict[str, type[ParsableFactory]] = {
            "401": ProblemDetails,
        }
        if not self.request_adapter:
            raise Exception("Http core is null") 
        from ....models.gateway_response import GatewayResponse

        return await self.request_adapter.send_async(request_info, GatewayResponse, error_mapping)
    
    def to_get_request_information(self,request_configuration: Optional[RequestConfiguration[SendMessagesRequestBuilderGetQueryParameters]] = None) -> RequestInformation:
        """
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: RequestInformation
        """
        request_info = RequestInformation(Method.GET, self.url_template, self.path_parameters)
        request_info.configure(request_configuration)
        return request_info
    
    def to_post_request_information(self,body: GatewayRequest, request_configuration: Optional[RequestConfiguration[QueryParameters]] = None) -> RequestInformation:
        """
        param body: The request body
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: RequestInformation
        """
        if body is None:
            raise TypeError("body cannot be null.")
        request_info = RequestInformation(Method.POST, '{+baseurl}/gw/rs/sendMessages', self.path_parameters)
        request_info.configure(request_configuration)
        request_info.headers.try_add("Accept", "application/json")
        request_info.set_content_from_parsable(self.request_adapter, "application/json", body)
        return request_info
    
    def with_url(self,raw_url: str) -> SendMessagesRequestBuilder:
        """
        Returns a request builder with the provided arbitrary URL. Using this method means any other path or query parameters are ignored.
        param raw_url: The raw URL to use for the request builder.
        Returns: SendMessagesRequestBuilder
        """
        if raw_url is None:
            raise TypeError("raw_url cannot be null.")
        return SendMessagesRequestBuilder(self.request_adapter, raw_url)
    
    @dataclass
    class SendMessagesRequestBuilderGetQueryParameters():
        def get_query_parameter(self,original_name: str) -> str:
            """
            Maps the query parameters names to their encoded names for the URI template parsing.
            param original_name: The original query parameter name in the class.
            Returns: str
            """
            if original_name is None:
                raise TypeError("original_name cannot be null.")
            if original_name == "batch_reference":
                return "BatchReference"
            if original_name == "message":
                return "Message"
            if original_name == "password":
                return "Password"
            if original_name == "service_id":
                return "ServiceId"
            if original_name == "username":
                return "Username"
            return original_name
        
        batch_reference: Optional[str] = None

        message: Optional[list[str]] = None

        password: Optional[str] = None

        service_id: Optional[int] = None

        username: Optional[str] = None

    
    @dataclass
    class SendMessagesRequestBuilderGetRequestConfiguration(RequestConfiguration[SendMessagesRequestBuilderGetQueryParameters]):
        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        warn("This class is deprecated. Please use the generic RequestConfiguration class generated by the generator.", DeprecationWarning)
    
    @dataclass
    class SendMessagesRequestBuilderPostRequestConfiguration(RequestConfiguration[QueryParameters]):
        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        warn("This class is deprecated. Please use the generic RequestConfiguration class generated by the generator.", DeprecationWarning)
    

