from typing import Any, Dict, List, Optional, Tuple
import ruamel.yaml
from pathlib import Path
import re, random, json
from caravel.baml.baml_client.type_builder import TypeBuilder, FieldType

from caravel.baml.baml_client.type_builder import TypeBuilder

class Parser:
    
    # let's think about what we will need to supply for a constructor here...
    def __init__(self, api_dict:Optional[Dict]=None, file:Optional[str]=""):
        self.openapi_spec = dict()
        self.path_map = dict()
        self.intents = list()
            
        if file != "":
            file_type = file.split(".")[-1]
            if file_type == "json":
                self.openapi_spec = self.json_to_dict(file)
            elif file_type == "yaml":
                file = self.yaml_to_json(in_file=file)
                self.openapi_spec = self.json_to_dict(file)
            else:
                raise ValueError("OpenAPI Specification file must be either JSON or YAML file. Ensure file uses .json or .yaml extension.")
        elif api_dict is not None:
            self.openapi_spec = api_dict
        if self.openapi_spec != {}:
            self.path_map = self.map_paths_to_desc(self.openapi_spec)
            self.intents = list(self.path_map.keys())
        
    def _clean_markdown(self, desc: str) -> str:
        '''
        Cleans up the OpenAPI description by removing unwanted markdown formatting.
        '''
        if not desc:
            return "N/A"
        
        desc = re.sub(r":::.*?:::", "", desc, flags=re.DOTALL)
        desc = re.sub(r"\n{2,}", " ", desc).strip()
        desc = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"\1 (\2)", desc)
        return desc
    
    def yaml_to_json(self, in_file: str, out_file: Optional[str]=f"output_{random.randint(1, 1000)}.json") -> None:
        yml = ruamel.yaml.YAML(typ='safe')
        with open(in_file) as fpi:
            data = yml.load(fpi)
        with open(out_file, 'w') as fpo:
            json.dump(data, fpo, indent=2)

    def json_to_dict(self, in_file: str) -> dict: 
        with open(in_file) as f:
            return json.load(f)
        
    def set_openapi_spec(self, spec: dict) -> None:
        self.openapi_spec = spec        
                
    def map_paths_to_desc(self, openapi_spec: dict) -> dict:
        
        for path, methods in openapi_spec["paths"].items():
            for method, details in methods.items():
                desc = details.get("summary", details.get("description", path))

                desc = self._clean_markdown(desc).split(".")[0] + "."
                formatted_key = f"{method.upper()} {desc}"

                self.path_map[formatted_key] = path
                
        return self.path_map
    
    
    
    # def resolve_ref(self, ref_path: str) -> dict:
    #     keys = ref_path.lstrip("#/").split("/")
    #     schema = self.openapi_spec
        
    #     for key in keys:
    #         schema = schema.get(key, {})
            
    #     if "$ref" in schema:
    #         return self.resolve_ref(schema["$ref"])
        
    #     return schema
    
    def resolve_ref(self, ref_path:str) -> dict:
        if not ref_path.startswith("#/"):
            raise ValueError(f"Invalid reference format: {ref_path}")
    
        keys = ref_path.lstrip("#/").split("/")
        schema = self.openapi_spec

        for key in keys:
            if key in schema:
                schema = schema[key]
            else:
                raise ValueError(f"Reference {ref_path} not found in schema.")
        
        # If the resolved schema itself has a $ref, resolve it recursively
        while "$ref" in schema:
            schema = self.resolve_ref(schema["$ref"])
            
        def resolve_nested_refs(obj):
            if isinstance(obj, dict):
                if "$ref" in obj:
                    return self.resolve_ref(obj["$ref"])
                return {key: resolve_nested_refs(value) for key, value in obj.items()}
            elif isinstance(obj, list):
                return [resolve_nested_refs(item) for item in obj]
            return obj
        
        if "properties" in schema:
            schema["properties"] = resolve_nested_refs(schema["properties"])
        return schema

    def extract_query_param_defaults(self, path: str, method: str) -> dict:
        query_param_defaults = {}
        
        query_params_schema = [
            p for p in self.openapi_spec["paths"][path][method].get("parameters", {}) if p.get("in", "") == "query"
        ]
        
        
        
        
        # populating
        for param in query_params_schema:
            name = param["name"]
            schema = param.get("schema", {})
            # query_param_defaults[name] = get_default_value(schema)
            possible_vals = self.get_default_value(schema)
            ### handle oneOf here
            if "oneOf" in schema:
                query_param_defaults[name] = " | ".join(possible_vals)
            else:
                query_param_defaults[name] = possible_vals
            
            
        return query_param_defaults

    def get_default_value(self, schema):
        
        if "$ref" in schema:
            schema = self.resolve_ref(schema["$ref"])
                
        if "enum" in schema:
            return " | ".join(schema["enum"])
            
        if "oneOf" in schema:
            # resolved_options = [resolve_ref(option["$ref"], openapi_spec) for option in schema["oneOf"]]
                # return {"oneOf": resolved_options}
            possible_keys = []
            for option in schema["oneOf"]:
                # resolved = self.resolve_ref(option["$ref"], self.openapi_spec) if "$ref" in option else option
                resolved = self.resolve_ref(option["$ref"]) if "$ref" in option else option
                if "properties" in resolved:
                    possible_keys.extend(resolved["properties"].keys())
            # the possible keys need to be represented with a union of each of their types
            # DO THAT HERE
            return possible_keys
            
        if "default" in schema:
            return schema["default"]            
            
        schema_type = schema.get("type")
        if schema_type == "string":
            return "<string>"
        elif schema_type == "integer":
            return 0 # needs to be @ least 1 for pagination
        elif schema_type == "boolean":
            return [True, False]
        elif schema_type == "number":
            return 0.0
        elif schema_type == "array":
            
            if "items" in schema:
                item_schema = schema["items"]
                resolved_item_schema = self.resolve_ref(item_schema["$ref"]) if "$ref" in item_schema else item_schema
            
            # Handle case where array items are objects
                if resolved_item_schema.get("type") == "object":
                    return [{key: self.get_default_value(value) for key, value in resolved_item_schema.get("properties", {}).items()}]
            
                return [self.get_default_value(resolved_item_schema)]
            return []
            
            
            # if "items" in schema:
            #     item_schema = schema["items"]
            #     if "$ref" in item_schema:
            #         resolved_item_schema = self.resolve_ref(item_schema["$ref"])
            #         return [self.get_default_value(resolved_item_schema)]
            #     elif "type" in item_schema:
            #         return [self.get_default_value(item_schema)]
            # return []
            # return ["<array>"]
        elif schema_type == "object":
            
            return {
                key: self.get_default_value(value) for key, value in schema.get("properties", {}).items()
                }
        return None
    
    
    class SchemaAdder:
        def __init__(self, tb: TypeBuilder, schema: Dict[str, Any], spec: dict):
            self.tb = tb
            self.schema = schema
            self._ref_cache = {}
            self.spec = spec
            self.existing_classes = set()

        def _parse_object(self, json_schema: Dict[str, Any], parent_key: str) -> FieldType:
            """Parses an object type from JSON schema, using the parent key to name the class."""

            # assert json_schema["type"] == "object"

            
            if not parent_key:
                raise ValueError("parent_key is required to name the object correctly.")

            # print(f"Parsing object: {parent_key}")  # Debugging output

            required_fields = json_schema.get("required", [])
            assert isinstance(required_fields, list)

            if parent_key in self.existing_classes:
                # print(f"Skipping duplicate class definition for {parent_key}")
                return self.tb.get_class(parent_key).type()

            self.existing_classes.add(parent_key)
            new_cls = self.tb.add_class(parent_key)

            if properties := json_schema.get("properties"):
                assert isinstance(properties, dict)

                for field_name, field_schema in properties.items():
                    assert isinstance(field_schema, dict)

                    default_value = field_schema.get("default")

                    # Recursively call parse, using the field name as the new parent_key
                    field_type = self.parse(field_schema, parent_key=field_name)

                    if field_name not in required_fields:
                        if default_value is None:
                            field_type = field_type.optional()

                    property = new_cls.add_property(field_name, field_type)

                    if description := field_schema.get("description"):
                        assert isinstance(description, str)
                        if default_value is not None:
                            description = (
                                description.strip() + "\n" + f"Default: {default_value}"
                            )
                            description = description.strip()
                        if len(description) > 0:
                            property.description(description)

            return new_cls.type()


        def _parse_string(self, json_schema: Dict[str, Any]) -> FieldType:
            # print("parsing string")
            assert json_schema["type"] == "string"
            title = json_schema.get("title")

            if enum := json_schema.get("enum"):
                return self.tb.union([self.tb.literal_string (value) for value in enum])
                # print("string is an enum")
                # assert isinstance(enum, list)
                # if title is None:
                #     print("title not given")
                #     # Treat as a union of literals
                #     return self.tb.union([self.tb.literal_string(value) for value in enum])
                # print(f"adding enum with title {title}")
                # new_enum = self.tb.add_enum(title)
                # for value in enum:
                #     new_enum.add_value(value)
                # return new_enum.type()
            return self.tb.string()

        def _load_ref(self, ref_path: str) -> FieldType:
            keys = ref_path.lstrip("#/").split("/")
            schema = self.spec

            for key in keys:
                schema = schema.get(key, {})

            if "$ref" in schema:
                return self._load_ref(schema["$ref"])

            # return self.parse(schema, parent_key=keys[-1])
            return schema

    
    
        def parse(self, json_schema: Dict[str, Any], parent_key:str=None) -> FieldType:
            if any_of := json_schema.get("anyOf"):
                assert isinstance(any_of, list)
                return self.tb.union([self.parse(sub_schema) for sub_schema in any_of])

            if ref := json_schema.get("$ref"):
                assert isinstance(ref, str)
                # return self._load_ref(ref)
                resolved_ref = self._load_ref(ref)
                ref_name = ref.split("/")[-1]
                return self.parse(resolved_ref, parent_key=ref_name)


            type_ = json_schema.get("type")
            if type_ is None:
                raise ValueError(f"Type is required in JSON schema: {json_schema}")
            parse_type = {
                "string": lambda: self._parse_string(json_schema),
                "number": lambda: self.tb.float(),
                "integer": lambda: self.tb.int(),
                "object": lambda: self._parse_object(json_schema, parent_key),
                "array": lambda: self.parse(json_schema["items"], parent_key).list() if "items" in  json_schema else self.tb.list_of(self.tb.any()),
                "boolean": lambda: self.tb.bool(),
                "null": lambda: self.tb.null(),
            }

            if type_ not in parse_type:
                raise ValueError(f"Unsupported type: {type_}")

            field_type = parse_type[type_]()
            # print(field_type)
            return field_type


    def parse_json_schema(self, json_schema: Dict[str, Any], tb: TypeBuilder, spec: dict) -> FieldType:
        parser = self.SchemaAdder(tb, json_schema, spec)
        return parser.parse(json_schema, parent_key="root")
    
    
    # def create_dynamic_type(self, schema, field_name:str="root"):
        
    #     if "$ref" in schema:
    #         schema = self.resolve_ref(schema["$ref"])
            
    #     if "oneOf" in schema:
    #         # resolved_options = [resolve_ref(option["$ref"], openapi_spec) for option in schema["oneOf"]]
    #             # return {"oneOf": resolved_options}
    #         possible_keys = []
    #         for option in schema["oneOf"]:
    #             # resolved = self.resolve_ref(option["$ref"], self.openapi_spec) if "$ref" in option else option
    #             resolved = self.resolve_ref(option["$ref"]) if "$ref" in option else option
    #             if "properties" in resolved:
    #                 possible_keys.extend(resolved["properties"].keys())
    #         # the possible keys need to be represented with a union of each of their types
    #         # DO THAT HERE
    #         return possible_keys
            
    #     # if "default" in schema:
    #         # return schema["default"]            
            
    #     schema_type = schema.get("type")
    #     print(f"{schema_type}")
    #     if schema_type == "string":
    #         if enum := schema.get("enum"):
    #             new_enum = self.tb.add_enum(field_name)
    #             for value in enum:
    #                 new_enum.add_value(value)
    #             return new_enum.type()
    #         return self.tb.string()
    #     elif schema_type == "integer":
    #         return self.tb.int()
    #     elif schema_type == "boolean":
    #         return self.tb.bool()
    #     elif schema_type == "number":
    #         return self.tb.float()
    #     elif schema_type == "array":
    #         if "items" in schema:
    #             item_schema = schema["items"]
    #             if "$ref" in item_schema:
    #                 resolved_item_schema = self.resolve_ref(item_schema["$ref"])
    #                 return [self.get_default_value(resolved_item_schema)]
    #             elif "type" in item_schema:
    #                 return [self.get_default_value(item_schema)]
    #         return []
    #         return ["<array>"]
    #     elif schema_type == "object":
    #         return {
    #             key: self.get_default_value(value, key) for key, value in schema.get("properties", {}).items()
    #             }
    #     return None
        
    def flatten_query_params(self, params: dict, prefix: str="") -> dict:
        flat_params = {}
        for key, value in params.items():
            full_key = f"{prefix}[{key}]" if prefix else key
            
            if isinstance(value, dict):
                flat_params.update(self.flatten_query_params(value, full_key))
            elif isinstance(value, list):
                if all(isinstance(item, str) for item in value):
                    joined_keys = " | ".join(value)
                    flat_params[f"{full_key}[{joined_keys}]"] = ""
            else:
                flat_params[full_key] = value
                
        return flat_params

    
    def extract_request_body(self, openapi_spec: dict, path: str, method: str) -> tuple:
        request_body = openapi_spec["paths"][path][method].get("requestBody", {}).get("content", {})
        # print("Request body reference: ", request_body)
        schema = request_body.get("application/json", {}).get("schema", {})
        # print("schema", schema)
        
        # resolve ref check
        if "$ref" in schema:
            schema = self.resolve_ref(schema["$ref"])
        
        # print("Post-resolve schema", schema)
        
        if not schema:
            return {}

        required_fields = schema.get("required", {})
        formatted_body = self.get_default_value(schema)
        return formatted_body, required_fields


    




# LEGACY -------------------------------
#     def create_api_dictionary(self, openapi_dict, cleanup_markdown=True, first_sentence=True, reformat=False):
#         # print(openapi_dict)
#         # print(openapi_dict.keys())
#         # print(openapi_dict.get("paths"))
#         for path, methods in openapi_dict.get("paths", {}).items():
#             print("Path: ", path)
#             for method, details in methods.items():
#                 print("method: ", method)
#                 if method.lower() not in ["put", "patch", "get", "post", "delete"]:
#                     continue
                
#                 # this will get query & path params
#                 pq_params = methods.get("parameters", [])
                
#                 description = details.get("description", "N/A").strip()
#                 print("Description: ", description)
                
#                 description = self._clean_markdown(desc=description).split(".")[0] + '.'
#                 print("Cleaned description: ", description)
                
#                 request_example = None
#                 required_params = []
#                 required_req = []
#                 properties={}
#                 print("example and required inited: ", request_example, required_params)
                
#                 if "requestBody" in details:
#                     print("requestBody found in details")
#                     content = details["requestBody"].get("content", {})
#                     print("content from requestBody: ", content)
#                     if "application/json" in content:
#                         print("application/json present in content")
#                         example_data = content["application/json"].get("example")
#                         examples_data = content["application/json"].get("examples", {}).values()

#                         if example_data:
#                             print("Example data:", example_data)
#                             request_example = example_data
#                         elif examples_data:
#                             print("Example data", examples_data[0].get("value"))
#                             request_example = examples_data[0].get("value")

#                         properties = content["application/json"].get('schema', {}).get("properties", {})
                        
#                         required_req = content["application/json"].get("schema", {}).get("required", [])
                        
#                 if "parameters" in details:
#                     print('"parameters" in details')
#                     required_params = [
#                         param["name"] for param in details["parameters"] if param.get("required", False)
#                     ]
#                     print("required params: ", required_params)
#                 key = f"{method.upper()} {description}"
#                 self.api_dictionary[key] = {
#                     "path": path,
#                     "parameters": pq_params,
#                     "properties": properties,
#                     "request_example": request_example,
#                     "required": required_params,
#                     "required_req": required_req
#                 }
#         return "Success"

# # NEELS code
#     # def create_api_dictionary_from_json(self, openapi_dict, cleanup_markdown=True, first_sentence=True, reformat=False):
#     #     '''
#     #     Parses an OpenAPI JSON Spec and extracts key details for each path.
        
#     #     Args:
#     #         openapi_json (dict): The OpenAPI spec as a dict.
        
#     #     Returns:
#     #         dict: A dictionary with paths as keys and the other info as values.
#     #     '''

#     #     parsed_data = dict()
#     #     paths = openapi_dict.get("paths", {})
        
#     #     for path, methods in paths.items():
#     #         for method, details in methods.items():
#     #             # Only concerned with CRUD ops
#     #             if method not in ["get", "post", "put", "delete", "patch"]:
#     #                 continue
                
#     #             # Extraction
#     #             description = details.get("description", "N/A")
#     #             required = []
#     #             request_example = None
                
                
#     #             parameters = details.get("parameters", [])
#     #             if parameters:
#     #                 print("PARAM:", parameters)
#     #             for param in parameters:
#     #                 if param.get("required", False):
#     #                     required.append(param["name"])
                
#     #             request_body = details.get("requestBody", {})
#     #             if request_body:
#     #                 print("REQ:",request_body)
#     #             content = request_body.get("content", {})
#     #             if "application/json" in content:
#     #                 examples = content["application/json"].get("example") or content["application/json"].get("examples", {})
#     #                 request_example = examples if examples else None
                
#     #             if cleanup_markdown:          
#     #                 description = self._clean_description(description)
#     #             if first_sentence:
#     #                 description = description.split(".")[0] + "."
#     #             if reformat:
#     #                 raise Exception("LLM Description Reformatting has not yet been implemented.")
            
#     #             if parsed_data.get(f"{description}", False):
#     #                 raise Exception("This key is already here.")
                            
#     #             parsed_data[f"{method.upper()} {description}"] = {
#     #                 "path": path,
#     #                 "request_example": request_example,
#     #                 "required": required
#     #             } # parsed_data
                        
#     #     self.api_dictionary = parsed_data
#     #     return parsed_data
        
#     # def get_schema_properties(self, ref_path, yaml_data, visited_refs=None):
        
#     #     if visited_refs is None:
#     #         visited_refs = set()

#     #     if not isinstance(ref_path, str) or not ref_path.startswith("#/ components/schemas/"):
#     #         return {"error": "Invalid $ref path"}

#     #     schema_name = ref_path.rsplit("/", 1)[-1]

#     #     if schema_name in visited_refs:
#     #         return {"error": "Circular reference detected", "schema":   schema_name}

#     #     while True:
#     #         if schema_name in visited_refs:
#     #             return {"error": "Circular reference detected", "schema":   schema_name}

#     #         visited_refs.add(schema_name)
#     #         schema = yaml_data.get("components", {}).get("schemas", {}).    get(schema_name)

#     #         if not isinstance(schema, dict):
#     #             return {"schema": schema_name, "properties": "No    properties found"}

#     #         if "properties" in schema:
#     #             return {"schema": schema_name, "properties": schema ["properties"]}

#     #         ref_path = schema.get("$ref")
#     #         if not ref_path:
#     #             return {"schema": schema_name, "properties": "No    properties found"}

#     #         schema_name = ref_path.rsplit("/", 1)[-1]
    
    
#     # def extract_yaml(self, api_dict = {}, yaml_data = None):
#     #     for path, methods in yaml_data.get("paths", {}).items():
#     #         for method, details in methods.items():
#     #             method_upper = method.upper()  # Convert HTTP method to     uppercase

#     #             if method_upper not in api_dict:
#     #                 api_dict[method_upper] = {}

#     #             # Initialize API path entry
#     #             api_dict[method_upper][path] = {
#     #                 "description": details.get("description", "No   description available"),
#     #                 "request_body_example": None  # Default value for   request body
#     #             }

#     #             # Check for request body example (for POST and PATCH    requests)
#     #             if method_upper in ["POST", "PUT", "PATCH", "DELETE"] and   "requestBody" in details:
#     #                 content = details["requestBody"].get("content", {})
#     #                 if "required" in content["application/json"]    ["schema"].keys():
#     #                     # print(content["application/json"]["schema"]   ["required"])
#     #                     api_dict[method_upper][path]["required"] = content  ["application/json"]["schema"]["required"]
#     #                 if "properties" in content["application/json"]  ["schema"].keys():
#     #                     api_dict[method_upper][path]    ["request_body_example"] = content["application/    json"]["schema"]["properties"]
#     #                 elif "$ref" in content["application/json"]["schema"].   keys() and "properties" not in content["application/   json"]["schema"].keys():
#     #                     properties = self.get_schema_properties(content  ["application/json"]["schema"]["$ref"],   yaml_data=yaml_data)
#     #                     api_dict[method_upper][path]    ["request_body_example"] = properties

#     #                 for content_type, content_details in content.items():
#     #                     # Check if 'example' is directly provided
#     #                     if "requestBody" in content_details:
#     #                         api_dict[method_upper][path]    ["request_body_example"] = content_details  ["requestBody"]
#     #                     # Check inside 'schema' for an example
#     #                     elif "schema" in content_details and "example" in   content_details["schema"]:
#     #                         api_dict[method_upper][path]    ["request_body_example"] = content_details  ["schema"]["example"]

#     #     return api_dict   
# ###

#     def get_api_dictionary(self):
#         '''
#         Returns the entire API dictionary.
#         '''
#         return self.api_dictionary

#     def get_api_entry(self, intent: str):
#         '''
#         Returns a single entry from the API Dictionary.
#         '''
#         return self.api_dictionary.get(intent, f"There is no valid route associated with the following intent: {intent}")
        
    
#     @staticmethod
#     def extract_openapi_json(path):
#         '''
#         Extracts the openapi json from the json file, converts it to a dict, and returns it.
#         '''
#         with open(f"{Path.cwd()}{path}", "r") as f:
#             openapi_dict = json.load(f)
#         return openapi_dict
    
#     @staticmethod
#     def make_openapi_json(yamlpath: str, jsonpath: str, indent:int=0):
#         '''
#         Converts an OpenAPI YAML file to an OpenAPI JSON file.
        
#         Args:
#             yamlpath (str): Path to the input YAML file.
#             jsonpath (str): Path to the output JSON file. 
#         '''
#         with open(f"{Path.cwd()}{yamlpath}", "r") as yml:
#             yaml_data = yaml.safe_load(yml)
#         with open(f"{Path.cwd()}{jsonpath}", "w") as jsn:
#             json.dump(yaml_data, jsn, indent=indent)
