from typing import Any, Optional, Union, Dict, List, Set, TypeVar, Generic
from pydantic import BaseModel

from at_common_workflow.core.context import Context

T = TypeVar('T')

class BaseMapping:
    """Base class for all mapping types."""
    
    def __eq__(self, other: object) -> bool:
        """
        Compare two mapping instances for equality.
        
        Args:
            other: Another mapping instance to compare with
            
        Returns:
            bool: True if the mappings are equal, False otherwise
        """
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__
    
    def __hash__(self) -> int:
        """
        Generate a hash value for this mapping.
        
        Returns:
            int: Hash value
        """
        return hash(tuple(sorted(self.__dict__.items())))
    
    def __repr__(self) -> str:
        attrs = ", ".join(f"{k}={v!r}" for k, v in self.__dict__.items())
        return f"{self.__class__.__name__}({attrs})"

class ArgumentMapping(BaseMapping):
    """Maps context values or constants to task arguments."""
    
    def __init__(self, value: Union[str, Any], dict_mapping: Optional[Dict[str, Union[str, Any]]] = None):
        self.value = value
        self.dict_mapping = dict_mapping
        self.is_context_ref = isinstance(value, str) and value.startswith("$")
        self.is_dict_mapping = dict_mapping is not None
        self._context_refs: Optional[List[str]] = None
    
    def get_context_refs(self) -> List[str]:
        """
        Get all context references used in this mapping.
        
        Returns:
            List[str]: List of context keys referenced by this mapping
        """
        # Cache the result for performance
        if self._context_refs is not None:
            return self._context_refs
            
        refs = []
        if self.is_context_ref:
            refs.append(self.value[1:])  # Remove $ prefix
        if self.is_dict_mapping:
            for value in self.dict_mapping.values():
                if isinstance(value, str) and value.startswith('$'):
                    refs.append(value[1:])
        
        self._context_refs = refs
        return refs
        
    def validate_context_refs(self, context: Context) -> List[str]:
        """
        Validate that all context references exist in the provided context.
        
        Args:
            context: Context object to validate references against
            
        Returns:
            List[str]: List of missing context keys
            
        Example:
            >>> missing_keys = arg_mapping.validate_context_refs(context)
            >>> if missing_keys:
            >>>     raise ValueError(f"Missing context keys: {missing_keys}")
        """
        if context is None:
            raise ValueError("Context cannot be None")
            
        missing_keys = []
        for ref in self.get_context_refs():
            if ref not in context:
                missing_keys.append(ref)
                
        return missing_keys

    def resolve(self, context: Context) -> Any:
        """
        Resolve the mapping value from context if it's a reference.
        
        Args:
            context: Context object to resolve references from
            
        Returns:
            Any: Resolved value or dictionary of resolved values
            
        Raises:
            KeyError: If a referenced context key doesn't exist
            ValueError: If context is None
        """
        if context is None:
            raise ValueError("Context cannot be None")
            
        if self.is_dict_mapping and self.dict_mapping is not None:
            result = {}
            for key, context_key in self.dict_mapping.items():
                if isinstance(context_key, str) and context_key.startswith('$'):
                    try:
                        result[key] = context.get(context_key[1:])
                    except KeyError:
                        raise KeyError(f"Context key '{context_key[1:]}' not found for mapping key '{key}'")
                else:
                    result[key] = context_key
            return result
            
        if self.is_context_ref:
            try:
                return context.get(self.value[1:])
            except KeyError:
                raise KeyError(f"Context key '{self.value[1:]}' not found")
            
        return self.value

class ResultMapping(BaseMapping, Generic[T]):
    """Maps task results to context keys."""
    
    def __init__(self, context_key: str, result_path: Optional[str] = None):
        self.context_key = context_key
        self.result_path = result_path
    
    def store(self, context: Context, result: T) -> None:
        """
        Store the task result in the context.
        
        Args:
            context: Context object to store the result in
            result: Task result to store
            
        Raises:
            AttributeError: If result_path is specified but doesn't exist in the result
        """
        if self.result_path:
            if not hasattr(result, self.result_path):
                raise AttributeError(f"Result does not have attribute '{self.result_path}'")
            value = getattr(result, self.result_path)
        else:
            value = result
            
        context.set(self.context_key, value)