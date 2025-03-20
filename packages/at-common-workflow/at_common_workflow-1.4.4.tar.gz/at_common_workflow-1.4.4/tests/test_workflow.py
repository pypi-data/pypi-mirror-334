import pytest
from at_common_workflow.core.workflow import WorkflowBuilder
from at_common_workflow.core.constants import WorkflowEventType
from pydantic import BaseModel
import asyncio
import time
from typing import AsyncIterator, List, Dict, Any, Optional
import random

class AddInputModel(BaseModel):
    a: int
    b: int

class AddOutputModel(BaseModel):
    result: int

async def execute_add(input: AddInputModel) -> AsyncIterator[AddOutputModel]:
    yield AddOutputModel(result=input.a + input.b)

@pytest.mark.asyncio
async def test_task_builder_initialization():
    workflow = (WorkflowBuilder()
        .define_processing_task("add_task")
            .with_input_model(AddInputModel)
            .with_output_model(AddOutputModel)
            .with_execute_func(execute_func=execute_add)
            .with_constant_arg("a", 5)
            .with_constant_arg("b", 3)
        .add("add_task_result", "result")
        .build()
    )

    # Assert that the workflow is not None
    assert workflow is not None

    # Assert that the task was added to the workflow
    assert len(workflow.nodes) == 1  # Assuming only one task is added

    # Assert that the task's name is correct
    task_node = workflow.nodes[0]
    assert task_node.task.name == "add_task"

    # Assert that the input model is set correctly
    assert task_node.task.input_model is AddInputModel

    # Assert that the output model is set correctly
    assert task_node.task.output_model is AddOutputModel

    # Assert that the constant arguments are mapped correctly
    assert task_node.argument_mappings["a"].value == 5
    assert task_node.argument_mappings["b"].value == 3

    # Assert that the result mapping is set correctly
    assert task_node.result_mapping.context_key == "add_task_result"

@pytest.mark.asyncio
async def test_task_builder_with_description():
    workflow = (WorkflowBuilder()
        .define_processing_task("add_task")
            .with_description("Adds two numbers")
            .with_input_model(AddInputModel)
            .with_output_model(AddOutputModel)
            .with_execute_func(execute_add)
            .with_constant_arg("a", 5)
            .with_constant_arg("b", 3)
        .add("result")
        .build()
    )
    
    assert workflow.nodes[0].task.description == "Adds two numbers"

@pytest.mark.asyncio
async def test_task_builder_with_context_arg():
    workflow = (WorkflowBuilder()
        .define_processing_task("first_task")
            .with_input_model(AddInputModel)
            .with_output_model(AddOutputModel)
            .with_execute_func(execute_add)
            .with_constant_arg("a", 5)
            .with_constant_arg("b", 3)
        .add("first_result", "result")
        .define_processing_task("second_task")
            .with_input_model(AddInputModel)
            .with_output_model(AddOutputModel)
            .with_execute_func(execute_add)
            .with_context_arg("a", "first_result")
            .with_constant_arg("b", 2)
        .add("final_result", "result")
        .build()
    )
    
    assert len(workflow.nodes) == 2
    second_task = workflow.nodes[1]
    assert second_task.argument_mappings["a"].value == "$first_result"
    assert second_task.argument_mappings["b"].value == 2

@pytest.mark.asyncio
async def test_task_builder_invalid_input_model():
    class InvalidModel:  # Not a Pydantic model
        pass
    
    with pytest.raises(TypeError, match="input_model must be a Pydantic BaseModel class"):
        (WorkflowBuilder()
            .define_processing_task("invalid_task")
                .with_input_model(InvalidModel)
        )

@pytest.mark.asyncio
async def test_task_builder_missing_required_components():
    # Missing input model
    with pytest.raises(ValueError, match="Input model must be defined"):
        (WorkflowBuilder()
            .define_processing_task("incomplete_task")
                .with_output_model(AddOutputModel)
                .with_execute_func(execute_add)
                .with_constant_arg("a", 1)
                .with_constant_arg("b", 2)
            .add("result")
        )
    
    # Missing execute function
    with pytest.raises(ValueError, match="Execute function must be defined"):
        (WorkflowBuilder()
            .define_processing_task("incomplete_task")
                .with_input_model(AddInputModel)
                .with_output_model(AddOutputModel)
                .with_constant_arg("a", 1)
                .with_constant_arg("b", 2)
            .add("result")
        )

@pytest.mark.asyncio
async def test_task_builder_invalid_constant_arg():
    with pytest.raises(ValueError, match="Constant argument .* looks like a context reference"):
        (WorkflowBuilder()
            .define_processing_task("invalid_task")
                .with_input_model(AddInputModel)
                .with_output_model(AddOutputModel)
                .with_execute_func(execute_add)
                .with_constant_arg("a", "$invalid_ref")
        )

@pytest.mark.asyncio
async def test_multiple_tasks_workflow():
    # Create a more complex workflow with multiple tasks
    workflow = (WorkflowBuilder()
        .define_processing_task("task1")
            .with_input_model(AddInputModel)
            .with_output_model(AddOutputModel)
            .with_execute_func(execute_add)
            .with_constant_arg("a", 5)
            .with_constant_arg("b", 3)
        .add("result1", "result")
        .define_processing_task("task2")
            .with_input_model(AddInputModel)
            .with_output_model(AddOutputModel)
            .with_execute_func(execute_add)
            .with_context_arg("a", "result1")
            .with_constant_arg("b", 2)
        .add("final_result", "result")
        .build()
    )
    
    assert len(workflow.nodes) == 2
    
    # Verify first task
    task1 = workflow.nodes[0]
    assert task1.task.name == "task1"
    assert task1.argument_mappings["a"].value == 5
    assert task1.argument_mappings["b"].value == 3
    assert task1.result_mapping.context_key == "result1"
    assert task1.result_mapping.result_path == "result"
    
    # Verify second task
    task2 = workflow.nodes[1]
    assert task2.task.name == "task2"
    assert task2.argument_mappings["a"].value == "$result1"
    assert task2.argument_mappings["b"].value == 2
    assert task2.result_mapping.context_key == "final_result"
    assert task2.result_mapping.result_path == "result"

@pytest.mark.asyncio
async def test_task_builder_invalid_output_model():
    class InvalidModel:  # Not a Pydantic model
        pass
    
    with pytest.raises(TypeError, match="output_model must be a Pydantic BaseModel class"):
        (WorkflowBuilder()
            .define_processing_task("invalid_task")
                .with_input_model(AddInputModel)
                .with_output_model(InvalidModel)
        )

@pytest.mark.asyncio
async def test_task_builder_chaining():
    # Test that all builder methods return self for proper chaining
    builder = WorkflowBuilder().define_processing_task("chain_task")
    
    # Test each method returns the builder instance
    assert builder.with_description("test") is builder
    assert builder.with_input_model(AddInputModel) is builder
    assert builder.with_output_model(AddOutputModel) is builder
    assert builder.with_execute_func(execute_add) is builder
    assert builder.with_constant_arg("a", 1) is builder
    assert builder.with_context_arg("b", "some_key") is builder

@pytest.mark.asyncio
async def test_task_builder_result_paths():
    # Create a more complex output model for testing result paths
    class ComplexOutputModel(BaseModel):
        value: int
        nested: dict
        items: list

    async def complex_execute(input: AddInputModel) -> AsyncIterator[ComplexOutputModel]:
        yield ComplexOutputModel(
            value=input.a + input.b,
            nested={"result": input.a * input.b},
            items=[input.a, input.b]
        )

    workflow = (WorkflowBuilder()
        .define_processing_task("complex_task")
            .with_input_model(AddInputModel)
            .with_output_model(ComplexOutputModel)
            .with_execute_func(complex_execute)
            .with_constant_arg("a", 5)
            .with_constant_arg("b", 3)
        .add("result1", "value")  # Store just the value field
        .define_processing_task("nested_task")
            .with_input_model(AddInputModel)
            .with_output_model(ComplexOutputModel)
            .with_execute_func(complex_execute)
            .with_constant_arg("a", 2)
            .with_constant_arg("b", 4)
        .add("result2", "nested.result")  # Store nested field
        .build()
    )
    
    assert len(workflow.nodes) == 2
    assert workflow.nodes[0].result_mapping.result_path == "value"
    assert workflow.nodes[1].result_mapping.result_path == "nested.result"

@pytest.mark.asyncio
async def test_task_builder_duplicate_task_names():
    workflow_builder = WorkflowBuilder()
    
    # Add first task
    workflow_builder.define_processing_task("same_name") \
        .with_input_model(AddInputModel) \
        .with_output_model(AddOutputModel) \
        .with_execute_func(execute_add) \
        .with_constant_arg("a", 1) \
        .with_constant_arg("b", 2) \
    .add("result1")
    
    # Add second task with same name
    workflow_builder.define_processing_task("same_name") \
        .with_input_model(AddInputModel) \
        .with_output_model(AddOutputModel) \
        .with_execute_func(execute_add) \
        .with_constant_arg("a", 3) \
        .with_constant_arg("b", 4) \
    .add("result2")
    
    # Build should succeed as duplicate names are allowed
    workflow = workflow_builder.build()
    assert len(workflow.nodes) == 2
    assert workflow.nodes[0].task.name == "same_name"
    assert workflow.nodes[1].task.name == "same_name"

class UserInputModel(BaseModel):
    user_id: str
    user_data: dict

class UserOutputModel(BaseModel):
    processed: bool
    data: dict

async def process_user(input: UserInputModel) -> AsyncIterator[UserOutputModel]:
    yield UserOutputModel(
        processed=True,
        data={"id": input.user_id, **input.user_data}
    )

@pytest.mark.asyncio
async def test_task_builder_context_arg_variations():
    """Test different ways of using with_context_arg"""
    
    # Build workflow with both single and dictionary context mappings
    workflow = (WorkflowBuilder()
        .define_processing_task("process_user")
            .with_input_model(UserInputModel)
            .with_output_model(UserOutputModel)
            .with_execute_func(process_user)
            # Test single value context mapping
            .with_context_arg("user_id", "user.id")
            # Test dictionary context mapping
            .with_context_arg("user_data", {
                "role": "user.role",
                "settings": "user.settings",
                "preferences": "user.prefs"
            })
        .add("result")
        .build()
    )

    # Verify argument mappings were created correctly
    process_task = workflow.nodes[0]
    
    # Check single value mapping
    assert process_task.argument_mappings["user_id"].value == "$user.id"
    
    # Check dictionary mapping
    user_data_mapping = process_task.argument_mappings["user_data"]
    assert user_data_mapping.dict_mapping == {
        "role": "$user.role",
        "settings": "$user.settings",
        "preferences": "$user.prefs"
    }
    
    # Test actual execution
    workflow.context.set("user.id", "123")
    workflow.context.set("user.role", "admin")
    workflow.context.set("user.settings", {"theme": "dark"})
    workflow.context.set("user.prefs", {"notifications": True})
    
    # Execute workflow
    async for _ in workflow.execute():
        pass
    
    # Verify results
    result = workflow.context.get("result")
    assert result.processed == True
    assert result.data["id"] == "123"
    assert result.data["role"] == "admin"
    assert result.data["settings"] == {"theme": "dark"}
    assert result.data["preferences"] == {"notifications": True}

@pytest.mark.asyncio
async def test_task_builder_context_arg_dollar_prefix():
    """Test that dollar prefix handling works correctly"""
    workflow = (WorkflowBuilder()
        .define_processing_task("process_user")
            .with_input_model(UserInputModel)
            .with_output_model(UserOutputModel)
            .with_execute_func(process_user)
            # Test with and without dollar prefix
            .with_context_arg("user_id", "$user.id")
            .with_context_arg("user_data", {
                "role": "$user.role",
                "settings": "user.settings"  # No dollar prefix
            })
        .add("result")
        .build()
    )

    process_task = workflow.nodes[0]
    
    # Both should have dollar prefix in final mapping
    assert process_task.argument_mappings["user_id"].value == "$user.id"
    assert process_task.argument_mappings["user_data"].dict_mapping == {
        "role": "$user.role",
        "settings": "$user.settings"
    }

@pytest.mark.asyncio
async def test_task_builder_context_arg_nested_paths():
    """Test that deeply nested context paths work correctly"""
    workflow = (WorkflowBuilder()
        .define_processing_task("process_user")
            .with_input_model(UserInputModel)
            .with_output_model(UserOutputModel)
            .with_execute_func(process_user)
            .with_context_arg("user_id", "users.current.id")
            .with_context_arg("user_data", {
                "role": "users.current.roles.primary",
                "settings": "users.current.preferences.settings"
            })
        .add("result")
        .build()
    )

    # Set up nested context
    workflow.context.set("users.current.id", "123")
    workflow.context.set("users.current.roles.primary", "admin")
    workflow.context.set("users.current.preferences.settings", {"theme": "dark"})
    
    # Execute workflow
    async for _ in workflow.execute():
        pass
    
    # Verify results
    result = workflow.context.get("result")
    assert result.processed == True
    assert result.data["id"] == "123"
    assert result.data["role"] == "admin"
    assert result.data["settings"] == {"theme": "dark"}

@pytest.mark.asyncio
async def test_workflow_execution_error_handling():
    """Test that errors during task execution are properly handled."""
    
    async def failing_execute(input: AddInputModel) -> AsyncIterator[AddOutputModel]:
        yield AddOutputModel(result=input.a + input.b)  # Yield a value first
        raise ValueError("Simulated error")  # Then raise the error
    
    workflow = (WorkflowBuilder()
        .define_processing_task("failing_task")
            .with_input_model(AddInputModel)
            .with_output_model(AddOutputModel)
            .with_execute_func(failing_execute)
            .with_constant_arg("a", 5)
            .with_constant_arg("b", 3)
        .add("result")
        .build()
    )
    
    # Execute workflow and expect an error
    with pytest.raises(RuntimeError):
        async for _ in workflow.execute():
            pass

@pytest.mark.asyncio
async def test_workflow_cyclic_dependencies():
    """Test that cyclic dependencies are detected."""
    
    workflow_builder = WorkflowBuilder()
    
    # Add first task
    workflow_builder.define_processing_task("task1") \
        .with_input_model(AddInputModel) \
        .with_output_model(AddOutputModel) \
        .with_execute_func(execute_add) \
        .with_constant_arg("a", 1) \
        .with_context_arg("b", "result2") \
        .add("result1")
    
    # Add second task with dependency on first task's result
    workflow_builder.define_processing_task("task2") \
        .with_input_model(AddInputModel) \
        .with_output_model(AddOutputModel) \
        .with_execute_func(execute_add) \
        .with_context_arg("a", "result1") \
        .with_constant_arg("b", 2) \
        .add("result2")
    
    # Building should fail due to cyclic dependency
    with pytest.raises(ValueError, match="Cyclic dependencies detected"):
        workflow_builder.build()

@pytest.mark.asyncio
async def test_workflow_events():
    """Test that workflow events are emitted correctly."""
    
    workflow = (WorkflowBuilder()
        .define_processing_task("add_task")
            .with_input_model(AddInputModel)
            .with_output_model(AddOutputModel)
            .with_execute_func(execute_add)
            .with_constant_arg("a", 5)
            .with_constant_arg("b", 3)
        .add("result")
        .build()
    )
    
    events = []
    async for event in workflow.execute():
        events.append(event)
    
    # Verify events
    assert len(events) >= 3  # At least WORKFLOW_STARTED, TASK_STARTED, TASK_COMPLETED, WORKFLOW_COMPLETED
    assert events[0].type == WorkflowEventType.WORKFLOW_STARTED
    assert any(e.type == WorkflowEventType.TASK_STARTED and e.task_name == "add_task" for e in events)
    assert any(e.type == WorkflowEventType.TASK_COMPLETED and e.task_name == "add_task" for e in events)
    assert events[-1].type == WorkflowEventType.WORKFLOW_COMPLETED

@pytest.mark.asyncio
async def test_parallel_task_execution():
    """Test that independent tasks execute in parallel."""
    
    # Create a task that takes some time to complete
    async def slow_execute(input: AddInputModel) -> AsyncIterator[AddOutputModel]:
        await asyncio.sleep(0.1)  # Simulate work
        yield AddOutputModel(result=input.a + input.b)
    
    # Create a workflow with two independent tasks
    workflow = (WorkflowBuilder()
        .define_processing_task("task1")
            .with_input_model(AddInputModel)
            .with_output_model(AddOutputModel)
            .with_execute_func(slow_execute)
            .with_constant_arg("a", 1)
            .with_constant_arg("b", 2)
        .add("result1")
        .define_processing_task("task2")
            .with_input_model(AddInputModel)
            .with_output_model(AddOutputModel)
            .with_execute_func(slow_execute)
            .with_constant_arg("a", 3)
            .with_constant_arg("b", 4)
        .add("result2")
        .build()
    )
    
    # Execute and time it
    start_time = time.time()
    async for _ in workflow.execute():
        pass
    execution_time = time.time() - start_time
    
    # If tasks ran in parallel, execution time should be close to 0.1s
    # If they ran sequentially, it would be closer to 0.2s
    assert execution_time < 0.15  # Allow some margin for test overhead

class StreamingInputModel(BaseModel):
    count: int

class StreamingOutputModel(BaseModel):
    value: int

async def streaming_counter(input: StreamingInputModel) -> AsyncIterator[StreamingOutputModel]:
    """Example streaming task that yields numbers up to count."""
    for i in range(input.count):
        yield StreamingOutputModel(value=i)
        await asyncio.sleep(0.1)  # Simulate some processing time

@pytest.mark.asyncio
async def test_streaming_task():
    """Test that streaming tasks emit events correctly."""
    
    workflow = (WorkflowBuilder()
        .define_processing_task("counter")
            .with_input_model(StreamingInputModel)
            .with_output_model(StreamingOutputModel)
            .with_execute_func(streaming_counter)
            .with_constant_arg("count", 5)
        .add("final_count")
        .build()
    )
    
    events = []
    async for event in workflow.execute():
        events.append(event)
    
    # Verify events
    assert len(events) >= 7  # WORKFLOW_STARTED + TASK_STARTED + 5 TASK_PROGRESS + TASK_COMPLETED + WORKFLOW_COMPLETED
    assert events[0].type == WorkflowEventType.WORKFLOW_STARTED
    
    # Verify streaming events
    stream_events = [e for e in events if e.type == WorkflowEventType.TASK_PROGRESS]
    assert len(stream_events) == 5
    
    # Verify stream data values
    for i, event in enumerate(stream_events):
        assert event.task_name == "counter"
        assert event.task_data.value == i
    
    assert events[-1].type == WorkflowEventType.WORKFLOW_COMPLETED

@pytest.mark.asyncio
async def test_realtime_event_reporting():
    """Test that events are reported in real-time rather than batched at the end."""
    
    # Create a task that yields values with delays between them
    async def delayed_counter(input: StreamingInputModel) -> AsyncIterator[StreamingOutputModel]:
        for i in range(input.count):
            yield StreamingOutputModel(value=i)
            await asyncio.sleep(0.2)  # Significant delay between events
    
    workflow = (WorkflowBuilder()
        .define_processing_task("delayed_counter")
            .with_input_model(StreamingInputModel)
            .with_output_model(StreamingOutputModel)
            .with_execute_func(delayed_counter)
            .with_constant_arg("count", 3)
        .add("final_count")
        .build()
    )
    
    # Collect events with timestamps
    events_with_time = []
    start_time = time.time()
    
    async for event in workflow.execute():
        event_time = time.time() - start_time
        events_with_time.append((event, event_time))
    
    # Extract just the progress events with their timestamps
    progress_events = [(e, t) for e, t in events_with_time 
                      if e.type == WorkflowEventType.TASK_PROGRESS]
    
    # Verify we got the expected number of progress events
    assert len(progress_events) == 3
    
    # Check that events were received with appropriate timing
    # If events were batched at the end, all timestamps would be very close together
    # With real-time reporting, they should be spaced out by approximately the sleep time
    
    # First event should come relatively quickly
    assert progress_events[0][1] < 0.3  # Allow some overhead
    
    # Subsequent events should be spaced by approximately the sleep time
    for i in range(1, len(progress_events)):
        time_diff = progress_events[i][1] - progress_events[i-1][1]
        assert 0.15 < time_diff < 0.3  # Should be close to the 0.2s sleep time
    
    # The last progress event should be well before the end of execution
    # This verifies events weren't all held until the end
    last_event_time = events_with_time[-1][1]
    last_progress_time = progress_events[-1][1]
    assert last_event_time - last_progress_time > 0.1

@pytest.mark.asyncio
async def test_concurrent_streaming_tasks():
    """Test that multiple streaming tasks can report events in real-time concurrently."""
    
    # Create tasks with different speeds
    async def fast_counter(input: StreamingInputModel) -> AsyncIterator[StreamingOutputModel]:
        for i in range(input.count):
            yield StreamingOutputModel(value=i)
            await asyncio.sleep(0.1)  # Fast task
    
    async def slow_counter(input: StreamingInputModel) -> AsyncIterator[StreamingOutputModel]:
        for i in range(input.count):
            yield StreamingOutputModel(value=i * 10)
            await asyncio.sleep(0.2)  # Slow task
    
    # Build workflow with two independent streaming tasks
    workflow = (WorkflowBuilder()
        .define_processing_task("fast_task")
            .with_input_model(StreamingInputModel)
            .with_output_model(StreamingOutputModel)
            .with_execute_func(fast_counter)
            .with_constant_arg("count", 5)
        .add("fast_result")
        .define_processing_task("slow_task")
            .with_input_model(StreamingInputModel)
            .with_output_model(StreamingOutputModel)
            .with_execute_func(slow_counter)
            .with_constant_arg("count", 3)
        .add("slow_result")
        .build()
    )
    
    # Collect events with timestamps and task names
    events = []
    start_time = time.time()
    
    async for event in workflow.execute():
        event_time = time.time() - start_time
        events.append((event, event_time))
    
    # Extract progress events by task
    fast_events = [(e, t) for e, t in events 
                  if e.type == WorkflowEventType.TASK_PROGRESS and e.task_name == "fast_task"]
    slow_events = [(e, t) for e, t in events 
                  if e.type == WorkflowEventType.TASK_PROGRESS and e.task_name == "slow_task"]
    
    # Verify we got the expected number of events
    assert len(fast_events) == 5
    assert len(slow_events) == 3
    
    # Verify the events are interleaved - we should see events from both tasks
    # before either task completes
    
    # Get the time of the last event from each task
    last_fast_time = fast_events[-1][1]
    last_slow_time = slow_events[-1][1]
    
    # Get all events that occurred before both tasks completed
    early_events = [e for e, t in events if t < min(last_fast_time, last_slow_time)]
    
    # We should see progress events from both tasks in the early events
    fast_progress_in_early = any(e.type == WorkflowEventType.TASK_PROGRESS and e.task_name == "fast_task" 
                               for e in early_events)
    slow_progress_in_early = any(e.type == WorkflowEventType.TASK_PROGRESS and e.task_name == "slow_task" 
                               for e in early_events)
    
    assert fast_progress_in_early, "Should see progress events from fast task before both tasks complete"
    assert slow_progress_in_early, "Should see progress events from slow task before both tasks complete"
    
    # Verify that the fast task completes before the slow task
    # (since it has more iterations but runs twice as fast)
    fast_completed_event = next((e, t) for e, t in events 
                              if e.type == WorkflowEventType.TASK_COMPLETED and e.task_name == "fast_task")
    slow_completed_event = next((e, t) for e, t in events 
                              if e.type == WorkflowEventType.TASK_COMPLETED and e.task_name == "slow_task")
    
    # The fast task should complete in about 0.5s, the slow task in about 0.6s
    assert fast_completed_event[1] < slow_completed_event[1]

@pytest.mark.asyncio
async def test_streaming_task_error_handling():
    """Test that errors in streaming tasks are properly handled and reported."""
    
    async def streaming_with_error(input: StreamingInputModel) -> AsyncIterator[StreamingOutputModel]:
        # Yield a few values successfully
        for i in range(2):
            yield StreamingOutputModel(value=i)
            await asyncio.sleep(0.1)
        
        # Then raise an error
        raise ValueError("Simulated error in streaming task")
    
    workflow = (WorkflowBuilder()
        .define_processing_task("error_stream")
            .with_input_model(StreamingInputModel)
            .with_output_model(StreamingOutputModel)
            .with_execute_func(streaming_with_error)
            .with_constant_arg("count", 5)  # We'll only get to 2 before error
        .add("result")
        .build()
    )
    
    # Collect events until error
    events = []
    with pytest.raises(RuntimeError) as excinfo:
        async for event in workflow.execute():
            events.append(event)
    
    # Verify error message
    assert "task failure" in str(excinfo.value)
    
    # Verify we got the expected events before the error
    assert events[0].type == WorkflowEventType.WORKFLOW_STARTED
    assert any(e.type == WorkflowEventType.TASK_STARTED and e.task_name == "error_stream" for e in events)
    
    # We should have received 2 progress events before the error
    progress_events = [e for e in events if e.type == WorkflowEventType.TASK_PROGRESS]
    assert len(progress_events) == 2
    
    # Verify the progress event values
    assert progress_events[0].task_data.value == 0
    assert progress_events[1].task_data.value == 1
    
    # We should have a task failed event
    failed_events = [e for e in events if e.type == WorkflowEventType.TASK_FAILED]
    assert len(failed_events) == 1
    assert failed_events[0].task_name == "error_stream"
    assert isinstance(failed_events[0].error, ValueError)
    assert "Simulated error in streaming task" in str(failed_events[0].error)

class SlowTaskInputModel(BaseModel):
    delay: float
    task_id: str

class SlowTaskOutputModel(BaseModel):
    result: str
    task_id: str
    execution_time: float

async def execute_slow_task(input: SlowTaskInputModel) -> AsyncIterator[SlowTaskOutputModel]:
    start_time = time.time()
    await asyncio.sleep(input.delay)
    execution_time = time.time() - start_time
    yield SlowTaskOutputModel(
        result=f"Completed task {input.task_id} after {execution_time:.2f}s",
        task_id=input.task_id,
        execution_time=execution_time
    )

@pytest.mark.asyncio
async def test_large_workflow():
    """Test a workflow with many tasks."""
    # Create a workflow with 50 tasks
    builder = WorkflowBuilder()
    
    # Add 50 simple addition tasks
    num_tasks = 50
    for i in range(num_tasks):
        builder = (builder
            .define_processing_task(f"add_task_{i}")
                .with_input_model(AddInputModel)
                .with_output_model(AddOutputModel)
                .with_execute_func(execute_func=execute_add)
                .with_constant_arg("a", i)
                .with_constant_arg("b", i + 1)
            .add(f"result_{i}", "result")
        )
    
    workflow = builder.build()
    
    # Verify workflow structure
    assert len(workflow.nodes) == num_tasks
    
    # Execute the workflow
    events = []
    
    async for event in workflow.execute():
        events.append(event)
    
    # Verify all tasks completed
    assert len(events) > num_tasks  # Should have at least one event per task
    
    # Verify all results are stored in context
    for i in range(num_tasks):
        assert workflow.context.get(f"result_{i}") == 2 * i + 1  # a + b = i + (i + 1)

@pytest.mark.asyncio
async def test_tasks_with_different_speeds():
    """Test a workflow with tasks that execute at different speeds."""
    builder = WorkflowBuilder()
    
    # Fast task (no delay)
    (builder.define_processing_task("fast_task")
        .with_input_model(SlowTaskInputModel)
        .with_output_model(SlowTaskOutputModel)
        .with_execute_func(execute_func=execute_slow_task)
        .with_constant_arg("delay", 0.01)
        .with_constant_arg("task_id", "fast")
        .add("fast_result", "result"))
    
    # Add another task that extracts the execution time from the same result
    (builder.define_processing_task("fast_time_task")
        .with_input_model(SlowTaskInputModel)
        .with_output_model(SlowTaskOutputModel)
        .with_execute_func(execute_func=execute_slow_task)
        .with_constant_arg("delay", 0.01)
        .with_constant_arg("task_id", "fast")
        .add("fast_time", "execution_time"))
    
    # Medium task
    (builder.define_processing_task("medium_task")
        .with_input_model(SlowTaskInputModel)
        .with_output_model(SlowTaskOutputModel)
        .with_execute_func(execute_func=execute_slow_task)
        .with_constant_arg("delay", 0.1)
        .with_constant_arg("task_id", "medium")
        .add("medium_result", "result"))
    
    # Add another task that extracts the execution time from the same result
    (builder.define_processing_task("medium_time_task")
        .with_input_model(SlowTaskInputModel)
        .with_output_model(SlowTaskOutputModel)
        .with_execute_func(execute_func=execute_slow_task)
        .with_constant_arg("delay", 0.1)
        .with_constant_arg("task_id", "medium")
        .add("medium_time", "execution_time"))
    
    # Slow task
    (builder.define_processing_task("slow_task")
        .with_input_model(SlowTaskInputModel)
        .with_output_model(SlowTaskOutputModel)
        .with_execute_func(execute_func=execute_slow_task)
        .with_constant_arg("delay", 0.2)
        .with_constant_arg("task_id", "slow")
        .add("slow_result", "result"))
    
    # Add another task that extracts the execution time from the same result
    (builder.define_processing_task("slow_time_task")
        .with_input_model(SlowTaskInputModel)
        .with_output_model(SlowTaskOutputModel)
        .with_execute_func(execute_func=execute_slow_task)
        .with_constant_arg("delay", 0.2)
        .with_constant_arg("task_id", "slow")
        .add("slow_time", "execution_time"))
    
    workflow = builder.build()
    
    # Execute the workflow
    events = []
    
    async for event in workflow.execute():
        events.append(event)
    
    # Verify all tasks completed
    assert "fast_result" in workflow.context
    assert "medium_result" in workflow.context
    assert "slow_result" in workflow.context
    
    # Verify execution times
    assert workflow.context.get("fast_time") < workflow.context.get("medium_time")
    assert workflow.context.get("medium_time") < workflow.context.get("slow_time")
    
    # Check event order - tasks should complete in order of speed
    task_completion_order = []
    for event in events:
        if event.type == WorkflowEventType.TASK_COMPLETED:
            task_completion_order.append(event.task_name)
    
    # Fast should complete before medium, medium before slow
    fast_idx = task_completion_order.index("fast_task")
    medium_idx = task_completion_order.index("medium_task")
    slow_idx = task_completion_order.index("slow_task")
    
    assert fast_idx < medium_idx < slow_idx

class CancellableTaskInputModel(BaseModel):
    task_id: str
    iterations: int
    delay_per_iteration: float

class CancellableTaskOutputModel(BaseModel):
    task_id: str
    iteration: int
    is_complete: bool

async def execute_cancellable_task(input: CancellableTaskInputModel) -> AsyncIterator[CancellableTaskOutputModel]:
    for i in range(input.iterations):
        # Check if cancelled between iterations
        if asyncio.current_task().cancelled():
            yield CancellableTaskOutputModel(
                task_id=input.task_id,
                iteration=i,
                is_complete=False
            )
            return
            
        # Sleep a bit to simulate work
        await asyncio.sleep(input.delay_per_iteration)
        
        # Yield progress
        yield CancellableTaskOutputModel(
            task_id=input.task_id,
            iteration=i + 1,
            is_complete=(i + 1 == input.iterations)
        )

@pytest.mark.asyncio
async def test_workflow_cancellation():
    """Test cancelling a workflow during execution."""
    builder = WorkflowBuilder()
    
    (builder.define_processing_task("long_running_task")
        .with_input_model(CancellableTaskInputModel)
        .with_output_model(CancellableTaskOutputModel)
        .with_execute_func(execute_func=execute_cancellable_task)
        .with_constant_arg("task_id", "long_task")
        .with_constant_arg("iterations", 10)
        .with_constant_arg("delay_per_iteration", 0.1)
        .add("task_result", "is_complete"))
    
    workflow = builder.build()
    
    # Execute the workflow in a separate task so we can cancel it
    events = []
    
    # Create a task for the workflow execution
    execution_task = asyncio.create_task(
        collect_events(workflow, events)
    )
    
    # Wait a bit to let it start
    await asyncio.sleep(0.3)
    
    # Cancel the task
    execution_task.cancel()
    
    try:
        await execution_task
    except asyncio.CancelledError:
        pass
    
    # Check that we got some events but not all
    assert len(events) > 0
    assert len(events) < 10  # Should be fewer than the total iterations
    
    # Since we can't check for WORKFLOW_CANCELLED (it doesn't exist in the enum),
    # we'll just verify that we got some events but not all the expected ones
    task_started = False
    for event in events:
        if hasattr(event, 'task_name') and event.task_name == "long_running_task":
            task_started = True
            break
    
    assert task_started, "Task should have started before cancellation"
    
    # Clean up any pending tasks
    for task in asyncio.all_tasks():
        if task is not asyncio.current_task() and not task.done():
            task.cancel()
            try:
                # Give it a moment to clean up
                await asyncio.wait_for(task, timeout=0.1)
            except (asyncio.CancelledError, asyncio.TimeoutError):
                pass

async def collect_events(workflow, events_list):
    """Helper function to collect events from a workflow execution."""
    try:
        async for event in workflow.execute():
            events_list.append(event)
    except asyncio.CancelledError:
        # Handle cancellation gracefully
        pass
        
    return events_list

class TimeoutTaskInputModel(BaseModel):
    delay: float

class TimeoutTaskOutputModel(BaseModel):
    result: str

@pytest.mark.asyncio
async def test_task_timeout():
    """Test handling task timeouts."""
    # Create a workflow with a task that will timeout
    builder = WorkflowBuilder()
    
    # Since with_timeout is not available, we'll simulate a timeout by using a custom task
    # that checks the elapsed time and raises a TimeoutError if it exceeds the limit
    
    async def timeout_aware_task(input: TimeoutTaskInputModel) -> AsyncIterator[TimeoutTaskOutputModel]:
        start_time = time.time()
        timeout_limit = 0.1  # 100ms timeout
        
        # Sleep for the requested delay
        await asyncio.sleep(min(input.delay, 0.01))  # Small sleep to allow for task to start
        
        # Check if we've exceeded the timeout
        elapsed = time.time() - start_time
        if elapsed + input.delay > timeout_limit:
            # Simulate a timeout by raising a TimeoutError
            raise asyncio.TimeoutError(f"Task timed out after {elapsed:.2f}s")
            
        # Complete the full delay
        await asyncio.sleep(input.delay - 0.01)
        yield TimeoutTaskOutputModel(result="Completed")
    
    (builder.define_processing_task("timeout_task")
        .with_input_model(TimeoutTaskInputModel)
        .with_output_model(TimeoutTaskOutputModel)
        .with_execute_func(execute_func=timeout_aware_task)
        .with_constant_arg("delay", 0.5)  # Task takes 0.5 seconds, but will timeout at 0.1
        .add("timeout_result", "result"))
    
    workflow = builder.build()
    
    # Execute the workflow
    events = []
    
    # We expect a RuntimeError due to the TimeoutError in the task
    with pytest.raises(RuntimeError) as excinfo:
        async for event in workflow.execute():
            events.append(event)
    
    # Verify the error message contains the task name
    assert "timeout_task" in str(excinfo.value)
    
    # Result should not be in context
    assert "timeout_result" not in workflow.context