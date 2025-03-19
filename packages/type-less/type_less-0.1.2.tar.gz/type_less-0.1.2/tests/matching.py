from typing import get_type_hints, get_origin, get_args, Literal, TypeVar, Union
import types

def is_equivalent_type(type1, type2):
    """
    Determine if two Python types are equivalent, handling complex nested types.
    
    This function compares two types for equivalence, including:
    - Basic types (int, str, etc.)
    - Generic types (List, Dict, etc.)
    - Union types (Union[int, str], Optional[int], etc.)
    - TypedDict types with nested structure
    - Literal types
    - TypeVar with constraints
    - ForwardRef types
    - Callable types
    
    Args:
        type1: First type to compare
        type2: Second type to compare
        
    Returns:
        bool: True if types are equivalent, False otherwise
    """
    # Handle None type
    if type1 is None and type2 is None:
        return True
    
    # Handle direct equality (same type object)
    if type1 is type2:
        return True
    
    # Get origin types (for generics)
    origin1 = get_origin(type1)
    origin2 = get_origin(type2)
    
    # If one has origin and other doesn't, they're not equivalent
    if (origin1 is None) != (origin2 is None):
        return False
    
    # Special case for Optional and Union
    if {origin1, origin2} <= {Union, types.UnionType}:
        # Handle Optional[T] == Union[T, None]
        args1 = get_args(type1)
        args2 = get_args(type2)
        
        # Check if one is Optional (Union with None)
        has_none1 = type(None) in args1
        has_none2 = type(None) in args2
        
        if has_none1 != has_none2:
            return False
            
        # Compare non-None args
        non_none_args1 = [arg for arg in args1 if arg is not type(None)]
        non_none_args2 = [arg for arg in args2 if arg is not type(None)]
        
        if len(non_none_args1) != len(non_none_args2):
            return False
            
        # For Union, order doesn't matter
        args2_remaining = set(non_none_args2)
        for arg1 in non_none_args1:
            for arg2 in args2_remaining:
                if is_equivalent_type(arg1, arg2):
                    args2_remaining.remove(arg2)
                    break
            else:
                return False
        return True
    
    # Get arguments of generic types
    args1 = get_args(type1)
    args2 = get_args(type2)
    
    # If number of args differs, types are not equivalent
    if len(args1) != len(args2):
        return False
    
    # Special handling for TypedDict
    if hasattr(type1, "__annotations__") and hasattr(type2, "__annotations__"):
        # Check if both are TypedDict
        if hasattr(type1, "__total__") and hasattr(type2, "__total__"):
            # Check if totality is the same
            if type1.__total__ != type2.__total__:
                return False
            
            # Get annotations
            annotations1 = get_type_hints(type1)
            annotations2 = get_type_hints(type2)
            
            # Check if keys match
            if set(annotations1.keys()) != set(annotations2.keys()):
                return False
            
            # Check if field types match
            return all(is_equivalent_type(annotations1[key], annotations2[key]) for key in annotations1)
    
    # Handle Literal
    if origin1 is Literal and origin2 is Literal:
        # For Literal, order doesn't matter but values must be identical
        return set(args1) == set(args2)
    
    # Handle Callable
    if origin1 in {types.FunctionType, callable} and origin2 in {types.FunctionType, callable}:
        if not args1 or not args2:
            return True  # Callable without specified signature
        
        if len(args1) != 2 or len(args2) != 2:
            return False
        
        # Compare parameter types
        params1, return1 = args1
        params2, return2 = args2
        
        # Handle Ellipsis in parameters
        if params1 is Ellipsis or params2 is Ellipsis:
            return is_equivalent_type(return1, return2)
        
        # If parameter counts differ, not equivalent
        if len(params1) != len(params2):
            return False
        
        # Check parameters and return type
        return all(is_equivalent_type(p1, p2) for p1, p2 in zip(params1, params2)) and \
               is_equivalent_type(return1, return2)
    
    # Handle basic types
    if origin1 is None and origin2 is None:
        if isinstance(type1, type) and isinstance(type2, type):
            return type1 is type2 or type1 == type2
        
        # Handle TypeVar
        if isinstance(type1, TypeVar) and isinstance(type2, TypeVar):
            return (type1.__name__ == type2.__name__ and 
                    type1.__constraints__ == type2.__constraints__ and
                    type1.__bound__ == type2.__bound__ and
                    type1.__covariant__ == type2.__covariant__ and
                    type1.__contravariant__ == type2.__contravariant__)
    
    # For other generic types, check if all arguments are equivalent
    # For tuples, order matters
    return all(is_equivalent_type(arg1, arg2) for arg1, arg2 in zip(args1, args2))



def validate_openapi_has_return_schema(openapi_spec: dict, path: str, method: Literal["get", "post", "put", "delete"]) -> bool:
    """
    Validates that the OpenAPI specification for a given endpoint matches the expected return type.
    
    Args:
        openapi_spec: The OpenAPI specification dictionary
        path: The API endpoint path
        method: The HTTP method (get, post, put)
        expected_type: The expected return type to validate against
        
    Returns:
        bool: True if the OpenAPI schema matches the expected type, False otherwise
    """
    # Check if the OpenAPI spec exists
    if not openapi_spec or "paths" not in openapi_spec:
        return False
    
    # Check if the path exists in the spec
    if path not in openapi_spec["paths"]:
        return False
    
    # Check if the method exists for the path
    path_spec = openapi_spec["paths"][path]
    if method not in path_spec:
        return False
    
    # Get the response schema
    method_spec = path_spec[method]
    if "responses" not in method_spec or "200" not in method_spec["responses"]:
        return False
    
    response_spec = method_spec["responses"]["200"]
    if "content" not in response_spec or "application/json" not in response_spec["content"]:
        return False
    
    schema = response_spec["content"]["application/json"].get("schema") or {}
    
    # For now, just check if schema exists
    return schema.get("$ref") is not None
