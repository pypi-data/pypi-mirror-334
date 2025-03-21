import asyncio
import time
import ssl
import orjson
import warnings
from langtools.core.logger import Logger, SDKLogger
from langtools.core.tracer import Tracer
from functools import wraps
from aiohttp import (
    ClientSession,
    TCPConnector,
    ClientTimeout,
    ClientError,
)
from typing import Optional, Mapping, Union, Dict, Any, Tuple, Type
from datetime import datetime
from azure.core.credentials import TokenCredential

# Suppress the RuntimeWarning about tracemalloc
warnings.filterwarnings("ignore", message=".*Event loop is closed.*")

class TokenCache:
    """Cache for access tokens with expiration handling"""
    def __init__(self):
        self._cache: Dict[str, Tuple[str, float]] = {}  # Changed to store timestamp
        self._lock = asyncio.Lock()

    async def get_token(self, scopeid: str) -> Optional[str]:
        """Get token from cache if not expired"""
        async with self._lock:
            if scopeid in self._cache:
                token, expiry = self._cache[scopeid]
                if time.time() < expiry:
                    return token
                del self._cache[scopeid]
            return None

    async def set_token(self, scopeid: str, token: str, expires_on: float):
        """Set token in cache with expiration"""
        async with self._lock:
            expiry = expires_on - 300  # 5 min buffer
            self._cache[scopeid] = (token, expiry)

class ResponseWrapper:
    """Wrapper for response that maintains access to content after client is closed"""
    def __init__(self, status: int, headers: Mapping, content: bytes, content_type: str = None):
        self._status = status
        self._headers = headers
        self._content = content
        self._content_type = content_type
        self._text = None
        self._json = None

    @property
    def status(self) -> int:
        return self._status

    @property
    def headers(self) -> Mapping:
        return self._headers

    @property
    def content(self) -> bytes:
        return self._content

    @property
    def content_type(self) -> Optional[str]:
        return self._content_type

    def json(self) -> Any:
        if self._json is None:
            self._json = orjson.loads(self._content)
        return self._json

    def text(self) -> str:
        if self._text is None:
            self._text = self._content.decode('utf-8')
        return self._text

class BaseConnector:
    def __init__(self, token_credential: Optional[TokenCredential] = None, logger=None, tracer=None, metric_counter=None,
                 total_timeout: float = 300, connect_timeout: float = 5):
        """Initialize the BaseConnector.

        Args:
            token_credential (Optional[TokenCredential]): Token credential for authentication
            logger: Custom logger instance
            tracer: Custom tracer instance
            metric_counter: Custom metric counter instance
            total_timeout (float): Total timeout in seconds for HTTP requests. Defaults to 300.
            connect_timeout (float): Connect timeout in seconds. Defaults to 5.
        """
        self.token_credential = token_credential
        self.total_timeout = total_timeout
        self.connect_timeout = connect_timeout
        
        self.metric_counter = metric_counter
        self.client = None
        self._connector = None
        self._session_lock = asyncio.Lock()
        self._token_cache = TokenCache()
        self.default_headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

        if logger is None:
            Logger.basicConfig(level=Logger.INFO)
            logger = Logger.getLogger(self.__class__.__name__)
        self.logger = logger
        self.sdklogger = SDKLogger.getSdklogger()
        
        # Initialize the tracer if not provided
        if tracer is None:
            # Initialize tracer with service name matching the class name
            service_name = self.__class__.__name__
            self.tracer = Tracer.getTracer(service_name)
            self.logger.info(f"Initialized new tracer for service: {service_name}")
        else:
            self.tracer = tracer
            self.logger.debug("Using provided tracer instance")

        self._cleanup_lock = asyncio.Lock()

    def _ensure_event_loop(self) -> asyncio.AbstractEventLoop:
        """Ensure an event loop is available and return it"""
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        return loop

    def _run_async(self, coro):
        """Run an async coroutine in the current event loop"""
        loop = self._ensure_event_loop()
        if loop.is_running():
            raise RuntimeError("Cannot run async operation while loop is running")
        return loop.run_until_complete(coro)

    def __enter__(self):
        """Synchronous context manager entry"""
        self._run_async(self.open())
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Synchronous context manager exit"""
        if not self._is_loop_closed():
            self._run_async(self.close())

    async def __aenter__(self):
        """Asynchronous context manager entry"""
        await self.open()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        """Asynchronous context manager exit"""
        await self.close()

    # Resource Management Methods
    def _is_loop_closed(self):
        """Check if the current event loop is closed"""
        try:
            loop = asyncio.get_event_loop()
            return loop.is_closed()
        except RuntimeError:
            return True

    async def _make_client(self) -> ClientSession:
        """Create and configure a new aiohttp ClientSession"""
        self.logger.debug("Creating new aiohttp ClientSession")
        if self._is_loop_closed():
            self.logger.error("Cannot create client: Event loop is closed")
            self.sdklogger.error("Cannot create client: Event loop is closed")
            raise RuntimeError("Event loop is closed")

        self.logger.debug(f"Configuring client timeout (total={self.total_timeout}s, connect={self.connect_timeout}s) and SSL context")
        timeout = ClientTimeout(total=self.total_timeout, connect=self.connect_timeout)
        
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE

        if self._connector is None or self._connector.closed:
            self._connector = TCPConnector(
                limit=500,
                ssl=ssl_context,
                force_close=True,
                enable_cleanup_closed=True
            )

        session = ClientSession(
            connector=self._connector,
            timeout=timeout,
            raise_for_status=False,
            connector_owner=True,
            auto_decompress=True
        )

        self.client = session
        return session

    async def open(self) -> None:
        """Open a new client session if none exists or if current one is closed"""
        self.logger.debug("Attempting to open client session")
        async with self._session_lock:
            try:
                if self.client is None or self.client.closed:
                    self.logger.info("Creating new client session")
                    await self._make_client()
                    self.logger.info("Client session created successfully")
                else:
                    self.logger.debug("Using existing client session")
            except Exception as e:
                self.logger.error(f"Failed to open client session: {str(e)}", exc_info=True)
                self.sdklogger.error(f"Failed to open client session: {str(e)}", exc_info=True)
                raise
    async def _cleanup_session(self):
        """Clean up session with proper error handling"""
        if not self._is_loop_closed():
            self.logger.debug("Starting client session cleanup")
            try:
                if self.client is not None and not self.client.closed:
                    self.logger.info("Closing active client session")
                    await self.client.close()
                    self.logger.info("Client session closed successfully")
            except Exception as e:
                self.logger.error(f"Failed to cleanup session: {str(e)}", exc_info=True)
                self.sdklogger.error(f"Failed to cleanup session: {str(e)}", exc_info=True)
            finally:
                self.logger.debug("Resetting client and connector references")
                self.client = None
                self._connector = None

    async def _cleanup(self):
        """Clean up resources with proper error handling"""
        async with self._cleanup_lock:
            self.logger.debug("Starting connector cleanup")
            try:
                if self._connector is not None and not self._connector.closed:
                    self.logger.info("Closing active connector")
                    await self._connector.close()
                    self.logger.info("Connector closed successfully")
                self._connector = None
            except Exception as e:
                self.logger.error(f"Failed to cleanup connector: {str(e)}", exc_info=True)
                self.sdklogger.error(f"Failed to cleanup connector: {str(e)}", exc_info=True)

    async def close(self) -> None:
        """Close the client and cleanup resources with proper error handling"""
        if not self._is_loop_closed():
            try:
                await self._cleanup_session()
                await self._cleanup()
            except Exception as e:
                self.logger.error(f"Error during cleanup: {e}", exc_info=True)
                self.sdklogger.error(f"Error during cleanup: {e}", exc_info=True)

    def __del__(self):
        """Ensure cleanup on object deletion"""
        try:
            loop = self._ensure_event_loop()
            if not loop.is_closed():
                loop.run_until_complete(self.close())
        except Exception:
            pass

    # Token Management Methods
    async def _get_token(self, scopeid: Optional[str] = None) -> str:
        """Get token from cache or credential with proper caching"""
        self.logger.debug(f"Attempting to get token for scope: {scopeid or 'default'}")
        
        # Use empty string as cache key when scopeid is None
        cache_key = scopeid if scopeid is not None else ""

        # Try to get token from cache
        cached_token = await self._token_cache.get_token(cache_key)
        if cached_token:
            self.logger.debug(f"Retrieved cached token for scope: {scopeid or 'default'}")
            return cached_token

        self.logger.info(f"No cached token found for scope: {scopeid or 'default'}, fetching new token")

        # Get new token and cache it
        token_response = self.token_credential.get_token() if scopeid is None else self.token_credential.get_token(scopeid)
        await self._token_cache.set_token(
            cache_key,
            token_response.token,
            token_response.expires_on  # expires_on is already a timestamp
        )
        return token_response.token

    def authenticate(self, token_credential: TokenCredential):
        """Set the token credential for the connector"""
        self.token_credential = token_credential
        self.logger.info("Token credential has been set.")

    # HTTP Request Methods
    async def http_call(self, method: str, url: str, stream: bool = False, **kwargs) -> Union[ResponseWrapper, ClientSession]:
        """Execute an HTTP call using a reusable session"""
        self.logger.info(f"Starting HTTP {method.upper()} request to {url}")
        
        if self._is_loop_closed():
            self.logger.error("Cannot execute request: Event loop is closed")
            self.sdklogger.error("Cannot execute request: Event loop is closed")
            raise RuntimeError("Event loop is closed")

        if self.client is None or self.client.closed:
            self.logger.debug("Opening new client session")
            await self.open()

        # Start with default headers
        headers = self.default_headers.copy()
        # Update with request-specific headers
        headers.update(kwargs.pop('headers', {}) or {})
        self.logger.debug(f"Request headers prepared: {headers}")
        
        scopeid = kwargs.pop('scopeid', None)
        if self.token_credential:
            token = await self._get_token(scopeid)
            headers['Authorization'] = f"Bearer {token}"

        max_retries = 3
        retry_delay = 1.0

        method = method.lower()
        http_method = getattr(self.client, method)

        last_error = None
        response = None
        wrapped_response = None

        try:
            for attempt in range(max_retries):
                try:
                    response = await http_method(url, headers=headers, **kwargs)
                    
                    if response.status >= 500:
                        await self._log_error_details(response, method, url)
                        
                        if attempt < max_retries - 1:
                            delay = retry_delay * (2 ** attempt)
                            self.logger.warning(
                                "HTTP %s call to %s failed with status %d. Retrying in %.1f seconds... (attempt %d/%d)",
                                method.upper(), url, response.status, delay, attempt + 1, max_retries
                            )
                            await response.close()
                            await asyncio.sleep(delay)
                            continue
                        break
                    
                    if response.status >= 400:
                        await self._log_error_details(response, method, url)
                        response.raise_for_status()
                    
                    self.logger.info("HTTP %s call to %s succeeded with status %d", method.upper(), url, response.status)
                    
                    # For streaming responses, return the raw response
                    if stream:
                        return response
                    
                    # For normal responses, wrap and return
                    wrapped_response = await self._wrap_response(response)
                    return wrapped_response

                except Exception as err:
                    try:
                        if response and not stream:
                            await response.close()
                    except Exception:
                        pass

                    last_error = err
                    if attempt < max_retries - 1 and getattr(err, "status", 0) >= 500:
                        delay = retry_delay * (2 ** attempt)
                        self.logger.warning(
                            "HTTP %s call to %s failed with error %s. Retrying in %.1f seconds... (attempt %d/%d)",
                            method.upper(), url, str(err), delay, attempt + 1, max_retries
                        )
                        await asyncio.sleep(delay)
                        continue
                    break

            if last_error:
                raise last_error
            raise ClientError("Max retries exceeded without error details")

        except Exception as e:
            try:
                if response and not stream:
                    await response.close()
            except Exception as cleanup_error:
                self.logger.debug(f"Error during response cleanup: {cleanup_error}")
                self.sdklogger.debug(f"Error during response cleanup: {cleanup_error}")
            raise

    async def _wrap_response(self, response) -> ResponseWrapper:
        """Create a ResponseWrapper from an aiohttp.ClientResponse"""
        if response is None:
            raise ClientError("No response received")
        content = await response.read()
        return ResponseWrapper(
            status=response.status,
            headers=response.headers,
            content=content,
            content_type=response.content_type
        )

    async def _log_error_details(self, response, method: str, url: str):
        """Log detailed error information from the response"""
        if response is None:
            self.logger.error(f"No response available for HTTP {method.upper()} request to {url}")
            self.sdklogger.error(f"No response available for HTTP {method.upper()} request to {url}")
            return

        try:
            self.logger.debug("Processing error response details")
            try:
                error_body = await response.text()
                try:
                    error_json = orjson.loads(error_body)
                    error_body = orjson.dumps(error_json, option=orjson.OPT_INDENT_2).decode('utf-8')
                    self.logger.debug("Successfully parsed error response as JSON")
                except orjson.JSONDecodeError:
                    self.logger.debug("Error response is not JSON format")
                    self.sdklogger.debug("Error response is not JSON format")
                    pass

                self.logger.error(
                    "HTTP %s request to %s failed with status %d\n"
                    "Response Headers:\n%s\n"
                    "Response Body:\n%s",
                    method.upper(),
                    url,
                    response.status,
                    orjson.dumps(dict(response.headers), option=orjson.OPT_INDENT_2).decode('utf-8'),
                    error_body
                )
            except Exception as e:
                self.logger.error(f"Error reading response: {e}")
                self.sdklogger.error(f"Error reading response: {e}")
        except Exception as e:
            self.logger.error(f"Failed to log error details: {e}", exc_info=True)
            self.sdklogger.error(f"Failed to log error details: {e}", exc_info=True)

    # Header Management Methods
    def update_header(self, key: str, value: str) -> None:
        """Update or add a single key-value pair to the default headers."""
        self.default_headers[key] = value
        self.logger.debug(f"Updated header {key} with value {value}")

    def set_default_headers(self, headers: Dict[str, str]) -> None:
        """Replace the entire default headers dictionary with a new one."""
        self.default_headers = headers.copy()
        self.logger.debug(f"Set new default headers: {headers}")