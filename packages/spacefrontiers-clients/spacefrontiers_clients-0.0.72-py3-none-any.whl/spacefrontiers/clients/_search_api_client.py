from aiobaseclient import BaseStandardClient
from izihawa_loglib.request_context import RequestContext
from izihawa_utils.common import filter_none
from spacefrontiers.clients.types import ConversationRequest, ConversationResponse


class SearchApiClient(BaseStandardClient):
    """Client for interacting with the Search API.

    A client that handles communication with the Search API endpoints, including authentication
    and request handling.

    Args:
        base_url (str): The base URL of the Search API.
        api_key (str | None, optional): API key for authentication. Defaults to None.
        user_id (str | int | None, optional): User ID of the user. Defaults to None.
        max_retries (int, optional): Maximum number of retry attempts. Defaults to 2.
        retry_delay (float, optional): Delay between retry attempts in seconds. Defaults to 0.5.
    """

    def __init__(
        self,
        base_url: str,
        api_key: str | None = None,
        user_id: str | int | None = None,
        max_retries: int = 2,
        retry_delay: float = 0.5,
        default_headers: dict[str, str] | None = None,
    ):
        """Initialize the SearchApiClient.

        Args:
            base_url (str): The base URL of the Search API.
            api_key (str | None, optional): API key for authentication. Defaults to None.
            user_id (str | int | None, optional): User ID of the user. Defaults to None.
            max_retries (int, optional): Maximum number of retry attempts. Defaults to 2.
            retry_delay (float, optional): Delay between retry attempts in seconds. Defaults to 0.5.
            default_headers (dict[str, str] | None, optional): Default headers for requests. Defaults to None.
        """
        if default_headers is None:
            default_headers = {}
        if api_key is not None:
            default_headers["X-Api-Key"] = api_key
        if user_id is not None:
            default_headers["X-User-Id"] = str(user_id)
        super().__init__(
            base_url=base_url,
            default_headers=default_headers,
            max_retries=max_retries,
            retry_delay=retry_delay,
        )

    async def post_conversations(
        self,
        conversation_request: ConversationRequest,
        timeout: float = 60.0,
        request_context: RequestContext | None = None,
    ) -> ConversationResponse:
        """Execute a conversation search request.

        Args:
            conversation_request (ConversationRequest): The conversation request parameters.
            timeout (float, optional): Request timeout in seconds. Defaults to 60.0.
            request_context (RequestContext | None, optional): Context for the request. Defaults to None.

        Returns:
            ConversationResponse: The conversation response
        """
        response = await self.post(
            "/v1/conversations/",
            json=filter_none(conversation_request.model_dump(exclude_none=True)),
            request_context=request_context,
            timeout=timeout,
        )
        return ConversationResponse(**response)
