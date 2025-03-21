from pythonnet import load
load("coreclr")

import clr
import os
import sys
import System
import asyncio
import warnings

from azure.identity import DefaultAzureCredential,CertificateCredential, ClientSecretCredential
from azure.core.credentials import TokenCredential
from msal import PublicClientApplication

from langtools.core.logger import Logger, SDKLogger
from langtools.core.tracer import Tracer

cur_path = os.path.dirname(os.path.abspath(__file__))
osclient_dll_path = os.path.join(cur_path, "linux-x64/")

sys.path.append(osclient_dll_path)
clr.AddReference("ObjectStoreClientCsharpLib")
from LangtoolsObjectStore import CsharpObjectStoreClient

clr.AddReference("System.Net.Http")
from System.Net import ServicePointManager, SecurityProtocolType
ServicePointManager.SecurityProtocol = SecurityProtocolType.Tls12

# Handling C# Async Task
from System.Threading.Tasks import Task
from System import Action

from langtools.core import Credential, CredentialType

class ObjectStoreClientError(Exception):
    """Base exception for BingGroundingClient errors."""
    pass


class ObjectStoreClient():
    """
    A Basic ObjectStore Client that currently only support Key-Value Store, with string key and string value.
    """
    def __init__(
        self,
        *,
        EnvironmentEndpoint: str,
        NamespaceName: str,
        TableName: str,
        cert_bytes: bytes,
        logger=None, tracer=None, metric_counter=None,
        **kwargs
    ) -> None:
        
        self.metric_counter = metric_counter
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

        self._client = CsharpObjectStoreClient(EnvironmentEndpoint, NamespaceName, TableName, cert_bytes)


    def close(self):
        """
        Close the ObjectStoreClient.
        """
        self._client.Dispose()
    
    def __enter__(self):
        return self  # Return the C# instance
    
    def __exit__(self, exc_type, exc_value, traceback):
        self._client.Dispose()  # Explicitly call Dispose() to free resources

    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_value, traceback):
        self._client.Dispose()

    def write(self, string_key: str, string_value: str) -> None:
        """
        Write a key-value pair to the ObjectStore.
        """
        self._client.Write(string_key, string_value)

    def read(self, string_key: str) -> str:
        """
        Read a value from the ObjectStore. The return is a json-format string.
        """
        return self._client.Read(string_key)
    
    async def read_async(self, string_key: str) -> str:
        """
        Read a value from the ObjectStore asynchronously. The return is a json-format string.
        """
        task = self._client.ReadAsync(string_key) #!! ReadAsync is a C# Task<String>, could not be wrapped by asyncio.to_thread or asyncio.wrap_future
        loop = asyncio.get_running_loop()
        future = loop.create_future()
        def callback(task):
            try:
                # Explicitly get the Result after task completion
                result = task.Result
                loop.call_soon_threadsafe(future.set_result, result)
            except Exception as e:
                loop.call_soon_threadsafe(future.set_exception, e)
         # Add continuation to handle task completion
        task.ContinueWith(Action[Task[str]](callback))
        return await future
    

    async def write_async(self, string_key: str, string_value: str) -> None:
        """
        Write a key-value pair to the ObjectStore asynchronously.
        """
        task = self._client.WriteAsync(string_key, string_value)  #!! WriteAsync is a C# Task, could not be wrapped by asyncio.to_thread or asyncio.wrap_future
        loop = asyncio.get_running_loop()
        future = loop.create_future()
        
        def callback(task):
            try:
                # For void Task, just check for exceptions
                if task.Exception:
                    loop.call_soon_threadsafe(
                        future.set_exception, task.Exception.InnerException
                    )
                else:
                    loop.call_soon_threadsafe(future.set_result, None)
            except Exception as e:
                loop.call_soon_threadsafe(future.set_exception, e)
        
        task.ContinueWith(Action[Task](callback))
        return await future