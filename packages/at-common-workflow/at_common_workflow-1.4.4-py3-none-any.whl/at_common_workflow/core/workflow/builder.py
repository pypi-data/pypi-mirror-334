import logging
from pathlib import Path
from typing import Optional, Dict, Any
from at_common_workflow.core.task import ProcessingTaskBuilder
from at_common_workflow.utils.logging import setup_logging
from .base import Workflow

class WorkflowBuilder:
    """Builder for creating and configuring workflows."""
    
    def __init__(self, logger: Optional[logging.Logger] = None):
        """
        Initialize a workflow builder.
        
        Args:
            logger: Optional logger to use for workflow logging
        """
        self.workflow = Workflow(logger=logger)
        # We'll keep track of task names but not enforce uniqueness
        self._task_names: Dict[str, int] = {}
    
    def define_processing_task(self, name: str) -> 'ProcessingTaskBuilder':
        """
        Add a task to the workflow and return a ProcessingTaskBuilder for configuring it.
        
        Args:
            name: Name for the task (doesn't need to be unique)
            
        Returns:
            ProcessingTaskBuilder: Builder for configuring the task
            
        Raises:
            ValueError: If name is empty
        """
        if not name:
            raise ValueError("Task name cannot be empty")
            
        # Track task names for debugging but allow duplicates
        self._task_names[name] = self._task_names.get(name, 0) + 1
            
        return ProcessingTaskBuilder(self, name=name)

    def build(self) -> Workflow:
        """
        Build and return the workflow.
        
        Returns:
            Workflow: The built and validated workflow
        
        Raises:
            ValueError: If the workflow has validation errors
        """
        # Validate the workflow before returning it
        try:
            self.workflow._build_dependency_graph()
        except Exception as e:
            raise ValueError(f"Workflow validation failed: {str(e)}") from e
            
        return self.workflow

    @classmethod
    def with_logging(cls, 
        level: int = logging.INFO,
        log_file: Optional[Path] = None,
        format_string: Optional[str] = None
    ) -> 'WorkflowBuilder':
        """
        Create a WorkflowBuilder with configured logging.
        
        Args:
            level: Logging level
            log_file: Optional path to log file
            format_string: Optional custom format string for log messages
            
        Returns:
            WorkflowBuilder: Configured builder instance
        """
        logger = setup_logging(level, log_file, format_string)
        return cls(logger=logger)