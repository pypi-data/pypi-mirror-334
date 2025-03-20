from typing import Type, Any, Callable, AsyncIterator, Awaitable, Dict, Optional
from .base import BaseTask, InputType, OutputType
from .validation import validate_task_configuration

class ProcessingTask(BaseTask[InputType, OutputType]):
    """
    Represents a processing task in a workflow with typed input and output.
    
    A processing task:
    - Accepts input conforming to a Pydantic model
    - Processes that input according to business logic
    - Produces output conforming to a Pydantic model
    - Can optionally stream data during processing
    """
    
    def __init__(
        self, 
        name: str,
        description: Optional[str] = None,
        input_model: Type[InputType] = None,
        output_model: Type[OutputType] = None,
        execute_func: Callable[[InputType], Awaitable[AsyncIterator[OutputType]]] = None
    ):
        """
        Initialize a processing task with its configuration.
        
        Args:
            name: Unique task name
            description: Optional task description
            input_model: Pydantic model class for input validation
            output_model: Pydantic model class for output validation
            execute_func: Async function that executes the task logic. Must return an async iterator
                        for streaming output.
        """
        super().__init__(name, description)
        self.input_model = input_model
        self.output_model = output_model
        self.execute_func = execute_func
        self._validate()
        
    def _validate(self) -> None:
        """Validate that task configuration is properly defined."""
        validate_task_configuration(
            self.name,
            self.input_model,
            self.output_model,
            self.execute_func
        )
    
    def __repr__(self) -> str:
        """String representation of the task."""
        return f"{self.__class__.__name__}(name={self.name!r}, description={self.description!r}) {self.input_model.__name__} -> {self.output_model.__name__}"
    
    def _validate_input(self, **kwargs) -> InputType:
        """
        Validate input arguments against input_model.
        
        Args:
            **kwargs: Input arguments
            
        Returns:
            Validated input model instance
            
        Raises:
            ValidationError: If input validation fails
        """
        try:
            return self.input_model(**kwargs)
        except Exception as e:
            raise ValueError(f"Input validation failed for task '{self.name}': {str(e)}") from e
    
    def _validate_output(self, output: Any) -> OutputType:
        """
        Validate output against output_model.
        
        Args:
            output: Task output
            
        Returns:
            Validated output model instance
            
        Raises:
            ValidationError: If output validation fails
        """
        try:
            if isinstance(output, self.output_model):
                return output
            return self.output_model(**output)
        except Exception as e:
            raise ValueError(f"Output validation failed for task '{self.name}': {str(e)}") from e
    
    async def __call__(self, **kwargs) -> AsyncIterator[OutputType]:
        """
        Allow tasks to be called directly for testing/debugging.
        Validates both input and output.
        
        Args:
            **kwargs: Input arguments
            
        Returns:
            An async iterator of validated outputs
            
        Raises:
            ValueError: If input or output validation fails
            Exception: Any exception raised during task execution
        """
        input_model = self._validate_input(**kwargs)
        
        try:
            result_gen = self.execute_func(input_model)
            
            async def validate_stream():
                async for item in result_gen:
                    try:
                        yield self._validate_output(item)
                    except Exception as e:
                        # Add task context to the error
                        raise ValueError(f"Output validation failed in task '{self.name}': {str(e)}") from e
            
            return validate_stream()
        except Exception as e:
            if not isinstance(e, ValueError) or "validation failed" not in str(e):
                # Only wrap non-validation errors
                raise ValueError(f"Execution failed in task '{self.name}': {str(e)}") from e
            raise