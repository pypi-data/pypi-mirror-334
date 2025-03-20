import pytest
from at_common_workflow.utils.mappings import ArgumentMapping, ResultMapping, BaseMapping
from at_common_workflow.core.context import Context

class TestBaseMapping:
    def test_equality(self):
        # Test equality comparison
        mapping1 = BaseMapping()
        mapping2 = BaseMapping()
        assert mapping1 == mapping2
        
        # Test inequality with different class
        class DifferentMapping(BaseMapping):
            pass
        
        different = DifferentMapping()
        assert mapping1 != different
    
    def test_hash(self):
        # Test hash functionality
        mapping1 = BaseMapping()
        mapping2 = BaseMapping()
        
        # Same mappings should have same hash
        assert hash(mapping1) == hash(mapping2)
        
        # Can be used as dict keys
        mappings = {mapping1: "value"}
        assert mappings[mapping2] == "value"
    
    def test_repr(self):
        # Test string representation
        mapping = BaseMapping()
        assert repr(mapping) == "BaseMapping()"

class TestArgumentMapping:
    def test_init(self):
        # Test initialization with constant
        const_mapping = ArgumentMapping("constant")
        assert const_mapping.value == "constant"
        assert not const_mapping.is_context_ref
        assert not const_mapping.is_dict_mapping
        
        # Test initialization with context reference
        ref_mapping = ArgumentMapping("$context_key")
        assert ref_mapping.value == "$context_key"
        assert ref_mapping.is_context_ref
        assert not ref_mapping.is_dict_mapping
        
        # Test initialization with dict mapping
        dict_mapping = ArgumentMapping(None, {"key1": "value1", "key2": "$context_key"})
        assert dict_mapping.value is None
        assert not dict_mapping.is_context_ref
        assert dict_mapping.is_dict_mapping
    
    def test_get_context_refs(self):
        # Test with constant
        const_mapping = ArgumentMapping("constant")
        assert const_mapping.get_context_refs() == []
        
        # Test with context reference
        ref_mapping = ArgumentMapping("$context_key")
        assert ref_mapping.get_context_refs() == ["context_key"]
        
        # Test with dict mapping
        dict_mapping = ArgumentMapping(None, {"key1": "value1", "key2": "$context_key"})
        assert dict_mapping.get_context_refs() == ["context_key"]
        
        # Test with both
        combined_mapping = ArgumentMapping("$outer_key", {"key1": "value1", "key2": "$inner_key"})
        refs = combined_mapping.get_context_refs()
        assert "outer_key" in refs
        assert "inner_key" in refs
        assert len(refs) == 2
    
    def test_validate_context_refs(self):
        # Setup context
        context = Context()
        context.set("existing_key", "value")
        
        # Test with all keys existing
        mapping = ArgumentMapping("$existing_key")
        assert mapping.validate_context_refs(context) == []
        
        # Test with missing keys
        mapping = ArgumentMapping("$missing_key")
        assert mapping.validate_context_refs(context) == ["missing_key"]
        
        # Test with dict mapping
        mapping = ArgumentMapping(None, {"key1": "$existing_key", "key2": "$missing_key"})
        missing = mapping.validate_context_refs(context)
        assert "missing_key" in missing
        assert len(missing) == 1
        
        # Test with None context
        with pytest.raises(ValueError):
            mapping.validate_context_refs(None)
    
    def test_resolve(self):
        # Setup context
        context = Context()
        context.set("string_key", "string_value")
        context.set("int_key", 42)
        context.set("dict_key", {"nested": "value"})
        
        # Test resolving constant
        mapping = ArgumentMapping("constant")
        assert mapping.resolve(context) == "constant"
        
        # Test resolving context reference
        mapping = ArgumentMapping("$string_key")
        assert mapping.resolve(context) == "string_value"
        
        mapping = ArgumentMapping("$int_key")
        assert mapping.resolve(context) == 42
        
        # Test resolving dict mapping
        mapping = ArgumentMapping(None, {
            "const_key": "constant",
            "ref_key": "$string_key",
            "int_ref": "$int_key"
        })
        result = mapping.resolve(context)
        assert result["const_key"] == "constant"
        assert result["ref_key"] == "string_value"
        assert result["int_ref"] == 42
        
        # Test error handling for missing keys
        mapping = ArgumentMapping("$missing_key")
        with pytest.raises(KeyError) as excinfo:
            mapping.resolve(context)
        assert "missing_key" in str(excinfo.value)
        
        # Test error handling for missing keys in dict mapping
        mapping = ArgumentMapping(None, {"key": "$missing_key"})
        with pytest.raises(KeyError) as excinfo:
            mapping.resolve(context)
        assert "missing_key" in str(excinfo.value)
        
        # Test error handling for None context
        mapping = ArgumentMapping("$key")
        with pytest.raises(ValueError) as excinfo:
            mapping.resolve(None)
        assert "Context cannot be None" in str(excinfo.value)

    def test_nested_context_references(self):
        """Test handling of nested context references."""
        context = Context()
        
        # Set up nested context values
        context.set("user", {"name": "John", "role": "admin"})
        context.set("roles", {"admin": {"permissions": ["read", "write"]}})
        
        # Test direct nested reference
        mapping = ArgumentMapping("$user.name")
        assert mapping.resolve(context) == "John"
        
        # Test reference to a value that is itself a reference
        context.set("user_role", "admin")  # Direct value instead of reference
        mapping = ArgumentMapping("$roles.$user_role.permissions")
        
        # The current implementation doesn't support nested references with $ in the path
        # So we'll test a workaround using dict mapping
        with pytest.raises(KeyError):
            mapping.resolve(context)
        
        # Workaround: Use a two-step approach
        user_role = context.get("user_role")
        permissions_path = f"roles.{user_role}.permissions"
        assert context.get(permissions_path) == ["read", "write"]
        
        # Test dict mapping with nested references
        mapping = ArgumentMapping(None, {
            "username": "$user.name",
            "permissions": "$roles.admin.permissions"  # Direct path instead of nested reference
        })
        result = mapping.resolve(context)
        assert result["username"] == "John"
        assert result["permissions"] == ["read", "write"]
        
        # Test validation of nested references
        assert mapping.validate_context_refs(context) == []
        
        # Test missing nested reference
        mapping = ArgumentMapping("$user.missing")
        assert "user.missing" in mapping.validate_context_refs(context)
    
    def test_complex_data_types(self):
        """Test handling of complex data types like functions or classes."""
        context = Context()
        
        # Define a function to store in context
        def test_function(x):
            return x * 2
        
        # Define a class to store in context
        class TestClass:
            def __init__(self, value):
                self.value = value
                
            def get_value(self):
                return self.value
        
        # Store complex types in context
        context.set("func", test_function)
        context.set("class", TestClass)
        context.set("instance", TestClass(42))
        
        # Test resolving function reference
        mapping = ArgumentMapping("$func")
        resolved_func = mapping.resolve(context)
        assert resolved_func(5) == 10
        
        # Test resolving class reference
        mapping = ArgumentMapping("$class")
        resolved_class = mapping.resolve(context)
        instance = resolved_class(21)
        assert instance.get_value() == 21
        
        # Test resolving instance reference
        mapping = ArgumentMapping("$instance")
        resolved_instance = mapping.resolve(context)
        assert resolved_instance.get_value() == 42
        
        # Test dict mapping with complex types
        mapping = ArgumentMapping(None, {
            "function": "$func",
            "class": "$class",
            "instance": "$instance"
        })
        result = mapping.resolve(context)
        assert result["function"](5) == 10
        assert result["class"](21).get_value() == 21
        assert result["instance"].get_value() == 42
    
    def test_none_values_in_dict_mapping(self):
        """Test handling of None values in dict mappings."""
        context = Context()
        context.set("null_value", None)
        context.set("valid_value", "value")
        
        # Test None as a constant value
        mapping = ArgumentMapping(None)
        assert mapping.resolve(context) is None
        
        # Test None in context
        mapping = ArgumentMapping("$null_value")
        assert mapping.resolve(context) is None
        
        # Test None in dict mapping values
        mapping = ArgumentMapping(None, {
            "null_constant": None,
            "null_reference": "$null_value",
            "valid_reference": "$valid_value"
        })
        result = mapping.resolve(context)
        assert result["null_constant"] is None
        assert result["null_reference"] is None
        assert result["valid_reference"] == "value"
        
        # Test None as dict mapping key - this is actually allowed in Python
        # but generally not recommended
        none_key_dict = {None: "value"}
        assert none_key_dict[None] == "value"
        
        # Verify ArgumentMapping can handle it
        mapping = ArgumentMapping(None, {None: "test_value"})
        assert mapping.dict_mapping[None] == "test_value"

class TestResultMapping:
    def test_init(self):
        # Test initialization with just context key
        mapping = ResultMapping("context_key")
        assert mapping.context_key == "context_key"
        assert mapping.result_path is None
        
        # Test initialization with result path
        mapping = ResultMapping("context_key", "result_path")
        assert mapping.context_key == "context_key"
        assert mapping.result_path == "result_path"
    
    def test_store(self):
        # Setup
        context = Context()
        
        # Test storing simple value
        mapping = ResultMapping("simple_key")
        mapping.store(context, "simple_value")
        assert context.get("simple_key") == "simple_value"
        
        # Test storing with result path
        class Result:
            def __init__(self):
                self.attribute = "attribute_value"
        
        result = Result()
        mapping = ResultMapping("attribute_key", "attribute")
        mapping.store(context, result)
        assert context.get("attribute_key") == "attribute_value"
        
        # Test error handling for invalid result path
        mapping = ResultMapping("error_key", "invalid_attribute")
        with pytest.raises(AttributeError) as excinfo:
            mapping.store(context, result)
        assert "invalid_attribute" in str(excinfo.value)
    
    def test_storing_complex_nested_objects(self):
        """Test storing complex nested objects."""
        context = Context()
        
        # Define a complex nested object
        class Address:
            def __init__(self, street, city):
                self.street = street
                self.city = city
        
        class Person:
            def __init__(self, name, address):
                self.name = name
                self.address = address
        
        # Create a nested object
        address = Address("123 Main St", "Anytown")
        person = Person("John Doe", address)
        
        # Store the entire object
        mapping = ResultMapping("person")
        mapping.store(context, person)
        assert context.get("person") == person
        
        # Store a nested attribute
        mapping = ResultMapping("person_address", "address")
        mapping.store(context, person)
        assert context.get("person_address") == address
        
        # Store a deeply nested attribute
        mapping = ResultMapping("person_city", "address.city")
        with pytest.raises(AttributeError):
            mapping.store(context, person)  # Current implementation doesn't support nested paths
        
        # Manually access nested attribute
        address = context.get("person_address")
        mapping = ResultMapping("city", "city")
        mapping.store(context, address)
        assert context.get("city") == "Anytown"
    
    def test_handling_inheritance(self):
        """Test handling inheritance in result objects."""
        context = Context()
        
        # Define a class hierarchy
        class Base:
            def __init__(self):
                self.base_attr = "base_value"
                
        class Derived(Base):
            def __init__(self):
                super().__init__()
                self.derived_attr = "derived_value"
                
        class DerivedFurther(Derived):
            def __init__(self):
                super().__init__()
                self.further_attr = "further_value"
        
        # Create instances
        base = Base()
        derived = Derived()
        further = DerivedFurther()
        
        # Test storing base class attribute from derived class
        mapping = ResultMapping("base_attr", "base_attr")
        mapping.store(context, derived)
        assert context.get("base_attr") == "base_value"
        
        # Test storing derived class attribute
        mapping = ResultMapping("derived_attr", "derived_attr")
        mapping.store(context, derived)
        assert context.get("derived_attr") == "derived_value"
        
        # Test storing attributes from multiple inheritance levels
        mapping = ResultMapping("further_base_attr", "base_attr")
        mapping.store(context, further)
        assert context.get("further_base_attr") == "base_value"
        
        mapping = ResultMapping("further_derived_attr", "derived_attr")
        mapping.store(context, further)
        assert context.get("further_derived_attr") == "derived_value"
        
        mapping = ResultMapping("further_attr", "further_attr")
        mapping.store(context, further)
        assert context.get("further_attr") == "further_value"
    
    def test_private_attributes(self):
        """Test storing results with private attributes."""
        context = Context()
        
        # Define a class with private attributes
        class PrivateClass:
            def __init__(self):
                self._private = "private_value"
                self.__dunder = "dunder_value"
                self.public = "public_value"
                
            def get_private(self):
                return self._private
                
            def get_dunder(self):
                return self.__dunder
        
        instance = PrivateClass()
        
        # Test storing public attribute
        mapping = ResultMapping("public_attr", "public")
        mapping.store(context, instance)
        assert context.get("public_attr") == "public_value"
        
        # Test storing private attribute (single underscore)
        mapping = ResultMapping("private_attr", "_private")
        mapping.store(context, instance)
        assert context.get("private_attr") == "private_value"
        
        # Test storing dunder attribute (double underscore)
        # Note: Python name mangling changes the actual attribute name
        mapping = ResultMapping("dunder_attr", "_PrivateClass__dunder")
        mapping.store(context, instance)
        assert context.get("dunder_attr") == "dunder_value"
        
        # Test storing via accessor methods
        # Methods are callable attributes, so they're stored as is
        mapping = ResultMapping("via_getter", "get_private")
        mapping.store(context, instance)
        
        # Verify that what was stored is the method itself, not its return value
        stored_method = context.get("via_getter")
        assert callable(stored_method)
        assert stored_method() == "private_value" 