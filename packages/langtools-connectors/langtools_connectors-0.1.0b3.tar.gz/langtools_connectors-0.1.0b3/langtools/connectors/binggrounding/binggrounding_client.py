from azure.core.credentials import TokenCredential
from ..base_connector import BaseConnector
import asyncio
import warnings
from typing import Union, Dict

# Suppress the RuntimeWarning about tracemalloc
warnings.filterwarnings('ignore', message='.*Enable tracemalloc.*')

class BingGroundingClientError(Exception):
    """Base exception for BingGroundingClient errors."""
    pass

class BingGroundingClient(BaseConnector):
    def __init__(
        self,
        *,
        token_credential: TokenCredential,
        scopeid: str = None,
        **kwargs
    ) -> None:
        if token_credential is None:
            raise BingGroundingClientError(
                "Missing token_credential. Please pass a valid TokenCredential instance."
            )

        # Call parent's __init__ first to set up logger
        super().__init__(
            token_credential=token_credential,
            logger=kwargs.get("logger"),
            tracer=kwargs.get("tracer"),
            metric_counter=kwargs.get("metric_counter")
        )

        # Initialize instance variables after super().__init__
        self.base_url = "https://www.bingapis.com/api/v2/grounding"
        self.scopeid = scopeid
        
        # Now we can use logger since it's initialized
        self.logger.info(f"Initializing BingGroundingClient with base_url: {self.base_url}")
        if scopeid:
            self.logger.debug(f"Using scope ID: {scopeid}")

        # Set headers after initialization
        self.default_headers.update({
            "Accept": "application/json",
            "Content-Type": "application/json",
        })
        self.search_async = self.tracer.search(self.search_async)
        self.search = self.tracer.search(self.search)
    
    def search(self, query: Union[str, Dict], **kwargs):
        """
        Perform a synchronous search query against the Bing Grounding API.
        This is a wrapper around the async search_async method.

        Args:
            query: Either a string query or a dictionary containing the complete JSON payload
            **kwargs: Additional arguments passed to the API as part of the JSON payload
                     e.g., maxGroundingResults, additionalContext, etc.
        """
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        try:
            result = loop.run_until_complete(self.search_async(query, **kwargs))
            return result
        except Exception as e:
            raise e

    async def search_async(self, query: Union[str, Dict], **kwargs):
        """
        Perform an asynchronous search query against the Bing Grounding API.
        Constructs and sends the search request using the BaseConnector's http_call.
        
        Args:
            query: Either a string query or a dictionary containing the complete JSON payload
            **kwargs: Additional arguments passed to the API as part of the JSON payload
                     e.g., maxGroundingResults, additionalContext, etc.
        
        Returns:
            ResponseWrapper: The response from the API
        """
        self.logger.info("Processing search query")
        self.logger.debug(f"Query details: {query}")

        url = f"{self.base_url}/search"
        headers = kwargs.pop("headers", {}) or {}
        
        if isinstance(query, str):
            self.logger.debug("Converting string query to JSON payload")
            data = {
                "query": query,
                **kwargs  # Include all remaining kwargs in the json payload
            }
        else:
            self.logger.debug("Using provided JSON payload")
            data = query

        # Only pass base arguments to http_call, put everything else in json payload
        call_kwargs = {
            'headers': headers,
            'json': data
        }
        
        # Use scopeid from constructor if not provided
        if self.scopeid and 'scopeid' not in kwargs:
            self.logger.debug(f"Using default scope ID: {self.scopeid}")
            call_kwargs['scopeid'] = self.scopeid
            
        self.logger.debug("Sending request to BingGrounding API")
        result = await self.http_call("post", url, **call_kwargs)
        self.logger.info("Successfully completed search request")
        return result