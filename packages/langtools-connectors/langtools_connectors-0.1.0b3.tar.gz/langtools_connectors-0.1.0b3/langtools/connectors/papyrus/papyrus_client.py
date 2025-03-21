from typing import Optional, Dict, Any, Union, List, AsyncGenerator, Generator
import orjson
import asyncio
from dataclasses import dataclass
from azure.core.credentials import TokenCredential
from ..base_connector import BaseConnector

class PapyrusClientError(Exception):
    """Base exception class for Papyrus client errors"""
    def __init__(self, message: str, original_exception: Exception = None):
        super().__init__(message)
        self.original_exception = original_exception

from openai.types.chat import (
    ChatCompletion,
    ChatCompletionChunk,
    ChatCompletionMessage,
    ChatCompletionMessageParam
)
from openai.types import (
    Completion,
    CreateEmbeddingResponse,
    Model
)

@dataclass
class Completions:
    """Completions API endpoint."""
    def __init__(self, client) -> None:
        self._client = client

    async def create(self, prompt: Union[str, List[str]], model: str, **kwargs) -> Completion:
        """Creates a completion for the provided prompt."""
        json_data = {
            "prompt": prompt,
            **kwargs
        }
        headers = {"papyrus-model-name": model}
        
        response = await self._client._make_request(
            "POST",
            "completions",
            headers=headers,
            json=json_data,
            stream=kwargs.get("stream", False)
        )
        if kwargs.get("stream", False):
            return response
        return Completion(**response.json())

@dataclass
class ChatCompletions:
    """Chat completions API endpoint."""
    def __init__(self, client) -> None:
        self._client = client

    async def create(
        self,
        messages: List[ChatCompletionMessageParam],
        model: str,
        **kwargs
    ) -> Union[ChatCompletion, AsyncGenerator[ChatCompletionChunk, None]]:
        """Creates a chat completion."""
        json_data = {
            "messages": messages,
            **kwargs
        }
        headers = {"papyrus-model-name": model}
        
        response = await self._client._make_request(
            "POST",
            "chat/completions",
            headers=headers,
            json=json_data,
            stream=kwargs.get("stream", False)
        )

        if kwargs.get("stream", False):
            async def stream_generator():
                try:
                    async for chunk in response.content:
                        if chunk:
                            chunk_str = chunk.decode('utf-8').strip()
                            self._client.logger.debug(f"Raw chunk: {chunk_str}")
                            
                            if not chunk_str:  # Skip empty chunks
                                continue
                                
                            if chunk_str.startswith('data: '):
                                chunk_str = chunk_str[6:].strip()  # Remove 'data: ' prefix
                            
                            if not chunk_str or chunk_str == '[DONE]':
                                continue
                                
                            try:
                                chunk_data = orjson.loads(chunk_str)
                                self._client.logger.debug(f"Parsed JSON data: {chunk_data}")
                                
                                # Ensure required fields are present and valid
                                chunk_data["object"] = "chat.completion.chunk"
                                if "id" not in chunk_data:
                                    chunk_data["id"] = "chatcmpl-default"
                                if "created" not in chunk_data:
                                    chunk_data["created"] = 0
                                if "model" not in chunk_data:
                                    chunk_data["model"] = model
                                if "choices" not in chunk_data:
                                    chunk_data["choices"] = []
                                if not chunk_data["choices"]:
                                    chunk_data["choices"].append({"delta": {}, "index": 0})
                                
                                # Ensure finish_reason has a valid value
                                for choice in chunk_data["choices"]:
                                    if "finish_reason" in choice and not choice["finish_reason"]:
                                        choice["finish_reason"] = "stop"
                                
                                self._client.logger.debug(f"Processed chunk data: {chunk_data}")
                                
                                # Create and validate chunk before yielding
                                chunk = ChatCompletionChunk(**chunk_data)
                                if chunk.choices and chunk.choices[0].delta:
                                    yield chunk
                                else:
                                    self._client.logger.debug("Skipping chunk without content")
                                    
                            except orjson.JSONDecodeError as e:
                                self._client.logger.debug(f"Skipping invalid JSON: '{chunk_str}' (Error: {e})")
                                continue
                            except Exception as e:
                                self._client.logger.error(f"Error processing chunk: {e}")
                                self._client.sdklogger.error(f"Error processing chunk: {e}")
                                self._client.logger.debug(f"Problematic chunk: {chunk_str}")
                                continue
                finally:
                    await response.release()
                    
            return stream_generator()

        return ChatCompletion(**response.json())

@dataclass
class Chat:
    """Chat API endpoint."""
    def __init__(self, client) -> None:
        self._client = client
        self.completions = ChatCompletions(client)

@dataclass
class Embeddings:
    """Embeddings API endpoint."""
    def __init__(self, client) -> None:
        self._client = client

    async def create(
        self,
        input: Union[str, List[str], List[int], List[List[int]]],
        model: str,
        **kwargs
    ) -> CreateEmbeddingResponse:
        """Creates embeddings for the provided input."""
        json_data = {
            "input": input,
            **kwargs
        }
        headers = {"papyrus-model-name": model}
        
        response = await self._client._make_request(
            "POST",
            "embeddings",
            headers=headers,
            json=json_data
        )
        return CreateEmbeddingResponse(**response.json())

@dataclass
class Models:
    """Models API endpoint."""
    def __init__(self, client) -> None:
        self._client = client

    async def list(self) -> List[Model]:
        """Lists the available models."""
        response = await self._client._make_request("GET", "models")
        data = response.json()
        return [Model(**model) for model in data.get("data", [])]

    async def retrieve(self, model: str) -> Model:
        """Retrieves a model instance."""
        headers = {"papyrus-model-name": model}
        response = await self._client._make_request(
            "GET",
            "models",
            headers=headers
        )
        return Model(**response.json())

class AsyncPapyrusClient(BaseConnector):
    """Asynchronous Papyrus client."""
    def __init__(
        self,
        azure_endpoint: str,
        token_credential: TokenCredential,
        scopeid: str,
        **kwargs
    ) -> None:
        if not azure_endpoint:
            raise PapyrusClientError("azure_endpoint is required")
        if not scopeid:
            raise PapyrusClientError("scopeid is required")

        super().__init__(
            token_credential=token_credential,
            logger=kwargs.get("logger"),
            tracer=kwargs.get("tracer"),
            metric_counter=kwargs.get("metric_counter")
        )

        self.base_url = azure_endpoint.rstrip('/')
        self.scopeid = scopeid

        self.logger.info(f"Initializing AsyncPapyrusClient with endpoint: {self.base_url}")
        self.logger.debug(f"Using scope ID: {self.scopeid}")
        
        # Set default headers for Azure OpenAI
        self.logger.debug("Setting up default headers")
        self.update_header("Content-Type", "application/json")

        # Initialize API endpoints
        self.logger.debug("Initializing API endpoints")
        self.completions = Completions(self)
        self.chat = Chat(self)
        self.embeddings = Embeddings(self)
        self.models = Models(self)
        self.chat.completions.create = self.tracer.llm(self.chat.completions.create)
        self.completions.create = self.tracer.llm(self.completions.create)
        self.embeddings.create = self.tracer.embedding(self.embeddings.create)

    async def _make_request(
        self,
        method: str,
        path: str,
        stream: bool = False,
        **kwargs
    ):
        """Make a request to the Azure OpenAI API."""
        url = f"{self.base_url}/{path}"
        self.logger.info(f"Making {method} request to {path}")
        self.logger.debug(f"Full URL: {url}")

        # Pass scopeid to http_call
        kwargs['scopeid'] = self.scopeid
        
        # Merge custom headers with any existing ones
        headers = kwargs.get('headers', {})
        if headers:
            self.logger.debug(f"Merging custom headers: {headers}")
            current_headers = self.default_headers.copy()
            current_headers.update(headers)
            kwargs['headers'] = current_headers
            
        return await self.http_call(method, url, stream=stream, **kwargs)

class SyncPapyrusClient(BaseConnector):
    """Synchronous Papyrus client with same interface as AsyncPapyrusClient."""
    def __init__(
        self,
        azure_endpoint: str,
        token_credential: TokenCredential,
        scopeid: str,
        **kwargs
    ) -> None:
        if not azure_endpoint:
            raise PapyrusClientError("azure_endpoint is required")
        if not scopeid:
            raise PapyrusClientError("scopeid is required")

        super().__init__(
            token_credential=token_credential,
            logger=kwargs.get("logger"),
            tracer=kwargs.get("tracer"),
            metric_counter=kwargs.get("metric_counter")
        )

        self.base_url = azure_endpoint.rstrip('/')
        self.scopeid = scopeid

        self.logger.info(f"Initializing SyncPapyrusClient with endpoint: {self.base_url}")
        self.logger.debug(f"Using scope ID: {self.scopeid}")
        
        # Set default headers for Azure OpenAI
        self.logger.debug("Setting up default headers")
        self.update_header("Content-Type", "application/json")

        # Initialize API endpoints with wrapped async methods
        self.logger.debug("Initializing API endpoints")
        self._setup_endpoints()

    def _setup_endpoints(self):
        """Set up API endpoints with wrapped async methods."""
        # Create endpoints
        completions = Completions(self)
        chat = Chat(self)
        embeddings = Embeddings(self)
        models = Models(self)
        
        chat.completions.create = self.tracer.llm(chat.completions.create)
        completions.create = self.tracer.llm(completions.create)
        embeddings.create = self.tracer.embedding(embeddings.create)
        # Wrap async methods
        completions.create = self._wrap_async(completions.create)
        chat.completions.create = self._wrap_async_stream(chat.completions.create)
        embeddings.create = self._wrap_async(embeddings.create)
        models.list = self._wrap_async(models.list)
        models.retrieve = self._wrap_async(models.retrieve)

        # Assign wrapped endpoints
        self.completions = completions
        self.chat = chat
        self.embeddings = embeddings
        self.models = models

    def _wrap_async(self, async_func):
        """Wrap an async function to make it synchronous."""
        def wrapper(*args, **kwargs):
            return self._run_async(async_func(*args, **kwargs))
        return wrapper

    def _wrap_async_stream(self, async_func):
        """Wrap an async function that may return an async generator."""
        def wrapper(*args, **kwargs):
            async_response = self._run_async(async_func(*args, **kwargs))

            if kwargs.get("stream", False):
                def sync_generator():
                    async_gen = async_response
                    while True:
                        try:
                            chunk = self._run_async(async_gen.__anext__())
                            yield chunk
                        except StopAsyncIteration:
                            break
                return sync_generator()
            
            return async_response
        return wrapper

    async def _make_request(
        self,
        method: str,
        path: str,
        stream: bool = False,
        **kwargs
    ):
        """Make a request to the Azure OpenAI API."""
        url = f"{self.base_url}/{path}"
        self.logger.info(f"Making {method} request to {path}")
        self.logger.debug(f"Full URL: {url}")

        # Pass scopeid to http_call
        kwargs['scopeid'] = self.scopeid
        
        # Merge custom headers with any existing ones
        headers = kwargs.get('headers', {})
        if headers:
            self.logger.debug(f"Merging custom headers: {headers}")
            current_headers = self.default_headers.copy()
            current_headers.update(headers)
            kwargs['headers'] = current_headers
            
        # Don't wrap the call in _run_async here since it's already being wrapped at the endpoint level
        return await self.http_call(method, url, stream=stream, **kwargs)

# For backwards compatibility
PapyrusClient = SyncPapyrusClient