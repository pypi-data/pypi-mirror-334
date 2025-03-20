from typing import List, Dict, Any

from chronulus_mcp.agent.forecaster import generate_model_from_fields, InputField


def detect_type_dependencies(schema: dict, target_type_names: List[str]) -> Dict[str, bool]:
    """
    Analyze a Pydantic model's JSON schema to detect fields that depend on a specific type.

    Parameters:
        schema: The json schema for the Pydantic data model
        target_type_names (List[str]): The names of the types to search for (e.g., 'ImageFromFile')

    Returns:
        Dict[str, bool]: Dictionary mapping field names to booleans indicating if they depend on any target type
    """
    dependencies = {}

    # Helper function for recursive schema analysis
    def check_schema_for_type(schema_part: Dict[str, Any], field_name: str = None) -> bool:
        # Check if this is a reference to a definition
        if '$ref' in schema_part:
            ref_path = schema_part['$ref']
            if ref_path.startswith('#/$defs/'):
                type_name = ref_path.split('/')[-1]
                if type_name in target_type_names:
                    return True

                # Check the referenced definition
                if type_name in schema.get('$defs', {}):
                    return check_schema_for_type(schema['$defs'][type_name], field_name)

        # Check for array types and analyze their items
        if schema_part.get('type') == 'array' and 'items' in schema_part:
            return check_schema_for_type(schema_part['items'], field_name)

        # Check for anyOf, oneOf, allOf arrays
        for array_key in ['anyOf', 'oneOf', 'allOf']:
            if array_key in schema_part and isinstance(schema_part[array_key], list):
                for item in schema_part[array_key]:
                    if isinstance(item, dict) and check_schema_for_type(item, field_name):
                        return True

        # Check title or additional properties that might indicate the type
        if schema_part.get('title', 'n/a') in target_type_names:
            return True

        # For custom types, check the format or additional properties
        for key, value in schema_part.items():
            if isinstance(value, dict):
                if check_schema_for_type(value, field_name):
                    return True
            elif isinstance(value, str) and value in target_type_names:
                return True

        return False

    # Check each property in the schema
    properties = schema.get('properties', {})
    for field_name, field_schema in properties.items():
        dependencies[field_name] = check_schema_for_type(field_schema, field_name)

    return dependencies


input_data_model = [
    InputField(name="image", description="Images", type="List[ImageFromFile]"),
    InputField(name="product", description="Product name", type="str")
]

InputItem = generate_model_from_fields("InputItem", input_data_model)




inputs = InputItem(**dict(image=[{"file_path":"/Users/theoldfather/Desktop/AIWorkspace/running-shoes/image.png"}]), product='shoes')


detect_type_dependencies(
            inputs.model_json_schema(mode="serialization"),
            ['ImageFromFile', 'ImageFromBytes', 'Image']
        )