from typing import Type, Callable, Any, Optional
from inspect import signature, isasyncgenfunction
from pydantic import BaseModel
from typing import AsyncIterator
from collections.abc import AsyncIterator as AsyncIteratorABC

def validate_task_configuration(
    name: str,
    input_model: Optional[Type],
    output_model: Optional[Type],
    execute_func: Optional[Callable]
) -> None:
    """
    Validate task configuration parameters.
    
    Args:
        name: Task name
        input_model: Input model class
        output_model: Output model class
        execute_func: Task execution function
        
    Raises:
        TypeError: If any parameter has an invalid type
        ValueError: If any parameter has an invalid value
    """
    # Validate name
    if not isinstance(name, str):
        raise TypeError("Task name must be a string")
    if not name.strip():
        raise ValueError("Task name cannot be empty")
    
    # Validate models
    if input_model is None:
        raise ValueError("Input model cannot be None")
    if output_model is None:
        raise ValueError("Output model cannot be None")
    
    if not isinstance(input_model, type):
        raise TypeError(f"input_model must be a class, got {type(input_model).__name__}")
    if not isinstance(output_model, type):
        raise TypeError(f"output_model must be a class, got {type(output_model).__name__}")
        
    if not issubclass(input_model, BaseModel):
        raise TypeError(f"input_model must be a Pydantic BaseModel subclass")
    if not issubclass(output_model, BaseModel):
        raise TypeError(f"output_model must be a Pydantic BaseModel subclass")
    
    # Validate execute function
    if execute_func is None:
        raise ValueError("execute_func cannot be None")
    if not callable(execute_func):
        raise TypeError(f"execute_func must be callable, got {type(execute_func).__name__}")
    
    # Check if the function is an async generator
    if not isasyncgenfunction(execute_func):
        raise TypeError("execute_func must be an async generator function (using 'async def' and 'yield')")
    
    # Validate function signature
    sig = signature(execute_func)
    params = list(sig.parameters.keys())
    
    if len(params) != 1:
        raise TypeError(f"execute_func must take exactly one parameter, got {len(params)}")
        
    if params[0] != 'input':
        raise TypeError(f"execute_func parameter must be named 'input', got '{params[0]}'")

    # Check return type annotation
    return_type = sig.return_annotation
    
    # Handle missing return type annotation
    if return_type is sig.empty:
        raise TypeError("execute_func must have a return type annotation")

    # Check if it's a direct output model
    if return_type == output_model:
        return

    # Check if it's an AsyncIterator of output model
    is_async_iterator = False
    element_type = None
    
    if hasattr(return_type, "__origin__"):
        if return_type.__origin__ is AsyncIterator or return_type.__origin__ is AsyncIteratorABC:
            is_async_iterator = True
            if hasattr(return_type, "__args__") and len(return_type.__args__) == 1:
                element_type = return_type.__args__[0]
    
    if is_async_iterator and element_type == output_model:
        return

    # If we get here, the return type is invalid
    raise TypeError(
        f"execute_func must return AsyncIterator[{output_model.__name__}], "
        f"got {return_type}"
    ) 