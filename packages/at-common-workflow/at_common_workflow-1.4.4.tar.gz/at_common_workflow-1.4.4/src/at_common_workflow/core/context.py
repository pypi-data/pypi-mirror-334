from typing import Any, Dict, Optional
from threading import RLock
import copy

class Context:
    """
    A dictionary-like class that stores key-value pairs throughout workflow execution.
    
    Features:
    - Supports dot notation access (e.g., context.user.name)
    - Supports nested keys using dot notation in strings (e.g., "user.name")
    - Raises KeyError for missing or invalid paths
    """
    def __init__(self) -> None:
        self._data: Dict[str, Any] = {}
        self._lock = RLock()  # Using RLock to allow recursive locking
    
    def __getattr__(self, key: str) -> Any:
        """Access context values using attribute notation."""
        with self._lock:
            return self.get(key)
    
    def __setattr__(self, key: str, value: Any) -> None:
        if key in ('_data', '_lock'):
            super().__setattr__(key, value)
        else:
            with self._lock:
                self.set(key, value)
    
    def get(self, key: str, default: Optional[Any] = None) -> Any:
        """Get value using dot notation for nested access.
        
        Args:
            key: Key to look up, can use dot notation for nested access
            default: Value to return if key is not found. If not provided, raises KeyError
        
        Raises:
            KeyError: If the key is not found and no default value is provided
            AttributeError: If key is None
        """
        with self._lock:
            if key is None:
                raise AttributeError("Key cannot be None")
                
            if not key:
                raise KeyError("Key cannot be empty")
                
            parts = key.split('.')
            current = self._data
            
            for i, part in enumerate(parts):
                if not isinstance(current, dict):
                    if default is None:
                        path = '.'.join(parts[:i])
                        raise KeyError(f"Cannot access '{part}' in '{key}': '{path}' is not a dict")
                    return default
                    
                if part not in current:
                    if default is None:
                        raise KeyError(f"Key '{key}' not found in context")
                    return default
                    
                current = current[part]
                
            return current
    
    def set(self, key: str, value: Any) -> None:
        """Set value using dot notation for nested access."""
        with self._lock:
            if key is None:
                raise AttributeError("Key cannot be None")
                
            if not key:
                raise KeyError("Key cannot be empty")
                
            parts = key.split('.')
            current = self._data
            
            for part in parts[:-1]:
                if part not in current:
                    current[part] = {}
                elif not isinstance(current[part], dict):
                    # Convert non-dict to dict if needed for nested keys
                    current[part] = {}
                current = current[part]
                
            current[parts[-1]] = value
            
    def copy(self) -> 'Context':
        """
        Create a deep copy of this context.
        
        Returns:
            Context: A new Context instance with the same data
        """
        with self._lock:
            new_context = Context()
            new_context._data = copy.deepcopy(self._data)
            return new_context

    def __contains__(self, key: str) -> bool:
        """Support 'in' operator for checking key existence."""
        try:
            self.get(key)
            return True
        except (KeyError, AttributeError):
            return False
    
    def __repr__(self) -> str:
        """Provide readable string representation."""
        return f"Context({self._data})"