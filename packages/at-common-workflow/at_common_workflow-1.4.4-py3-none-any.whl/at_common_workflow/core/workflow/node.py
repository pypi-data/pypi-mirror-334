from typing import Dict, Set, Optional
from at_common_workflow.core.task import ProcessingTask
from at_common_workflow.utils import ArgumentMapping, ResultMapping
from at_common_workflow.core.exceptions import TaskValidationError

class Node:
    """Represents a task node in the workflow graph."""
    
    def __init__(
        self,
        task: ProcessingTask,
        argument_mappings: Dict[str, ArgumentMapping],
        result_mapping: ResultMapping
    ) -> None:
        """
        Initialize a workflow node.
        
        Args:
            task: The task to execute
            argument_mappings: Mappings for task arguments
            result_mapping: Mapping for task result
            
        Raises:
            TaskValidationError: If argument validation fails
        """
        if not task:
            raise ValueError("Task cannot be None")
        if not result_mapping:
            raise ValueError("Result mapping cannot be None")
            
        self._validate_arguments(task, argument_mappings)
        self.task = task
        self.argument_mappings = argument_mappings
        self.result_mapping = result_mapping
        self.dependencies: Set[str] = set()
    
    @staticmethod
    def _validate_arguments(task: ProcessingTask, argument_mappings: Dict[str, ArgumentMapping]) -> None:
        """
        Validate that all required arguments are provided.
        
        Args:
            task: The task to validate arguments for
            argument_mappings: The argument mappings to validate
            
        Raises:
            TaskValidationError: If required arguments are missing
        """
        if not hasattr(task.input_model, 'model_fields'):
            raise TaskValidationError(
                f"Input model for task {task.name} does not have model_fields attribute"
            )
            
        required_fields = {
            field_name for field_name, field in 
            task.input_model.model_fields.items()
            if field.is_required
        }
        
        missing_args = required_fields - argument_mappings.keys()
        if missing_args:
            raise TaskValidationError(
                f"Missing required arguments for task {task.name}: {missing_args}"
            )
            
    def __repr__(self) -> str:
        """String representation of the node."""
        return f"Node(task={self.task.name}, result_key={self.result_mapping.context_key})"