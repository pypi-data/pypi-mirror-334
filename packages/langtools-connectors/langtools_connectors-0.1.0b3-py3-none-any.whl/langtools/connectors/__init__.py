"""Connectors package."""
name = 'connectors'

from .base_connector import BaseConnector
import sys

class _LazyClient:
    """Proxy class that lazily loads the actual client implementation."""
    def __init__(self, module_name, class_name):
        self._module_name = module_name
        self._class_name = class_name
        self._actual_class = None
        
    def _load_class(self):
        """Load the actual class if not already loaded."""
        if self._actual_class is None:
            try:
                # Import the module containing the class
                __import__(self._module_name)  # First import the package
                module = sys.modules[self._module_name]  # Then get the module
                self._actual_class = getattr(module, self._class_name)
            except ImportError:
                # Ignore import errors from problematic modules
                # but raise import errors for the module being directly accessed
                if sys._getframe().f_back.f_code.co_name == '__call__':
                    raise
                return None
        return self._actual_class

    def __call__(self, *args, **kwargs):
        """Create and return an instance of the actual class."""
        actual_class = self._load_class()
        if actual_class is None:
            return None
        # Return the actual instance instead of the proxy
        return actual_class(*args, **kwargs)

    def __getattr__(self, name):
        """Handle access to static methods and class attributes."""
        actual_class = self._load_class()
        if actual_class is None:
            return None
        return getattr(actual_class, name)

# Create proxy objects for each client
AsyncPapyrusClient = _LazyClient('langtools.connectors.papyrus', 'AsyncPapyrusClient')
PapyrusClient = _LazyClient('langtools.connectors.papyrus', 'PapyrusClient')
PapyrusClientError = _LazyClient('langtools.connectors.papyrus', 'PapyrusClientError')
BingGroundingClient = _LazyClient('langtools.connectors.binggrounding', 'BingGroundingClient')
BingGroundingClientError = _LazyClient('langtools.connectors.binggrounding', 'BingGroundingClientError')
ObjectStoreClient = _LazyClient('langtools.connectors.objectstore_client', 'ObjectStoreClient')

__all__ = [
    # Base classes
    'BaseConnector',
    
    # Clients
    'BingGroundingClient',
    'AsyncPapyrusClient',
    'PapyrusClient',
    'ObjectStoreClient',
    
    # Errors
    'BingGroundingClientError',
    'PapyrusClientError'
]