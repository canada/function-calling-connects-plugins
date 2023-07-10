import yaml

class OpenApiToFunctionConverter:

    openapi_definition: str

    # コンストラクタ
    def __init__(self, yaml_file_path: str):
        # YAMLファイルを読み込む
        with open(yaml_file_path) as f:
            self.openapi_definition = f.read()

    # YAMLスキーマ中の$refを展開する
    @staticmethod
    def _resolve_schema(schema: str, components_schemas: dict) -> dict:
        if "$ref" in schema:
            ref_name = schema["$ref"].split("/")[-1]
            return OpenApiToFunctionConverter._resolve_schema(components_schemas[ref_name], components_schemas)
        elif "properties" in schema:
            resolved_properties = {}
            for prop_name, prop_schema in schema["properties"].items():
                resolved_properties[prop_name] = OpenApiToFunctionConverter._resolve_schema(prop_schema, components_schemas)
            schema["properties"] = resolved_properties
        elif "items" in schema:
            schema["items"] = OpenApiToFunctionConverter._resolve_schema(schema["items"], components_schemas)
        return schema

    # OpenAPI定義を関数定義に変換する
    @staticmethod
    def _convert_to_functions(openapi_definition: str) -> list:
        openapi_data = yaml.safe_load(openapi_definition)
        paths = openapi_data["paths"]
        components_schemas = openapi_data["components"]["schemas"]
        functions = []

        for path, methods in paths.items():
            for _, details in methods.items():
                function = {
                    "name": path.strip("/"),
                    "description": details["summary"],
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": [],
                    },
                    "responses": {},
                }

                for parameter in details["parameters"]:
                    param_name = parameter["name"]
                    function["parameters"]["properties"][param_name] = {
                        "type": parameter["schema"]["type"],
                        "description": parameter["description"],
                    }
                    if parameter["required"]:
                        function["parameters"]["required"].append(param_name)

                for response_code, response_details in details["responses"].items():
                    response_schema = response_details["content"]["application/json"]["schema"]
                    resolved_schema = OpenApiToFunctionConverter._resolve_schema(response_schema, components_schemas)
                    function["responses"][response_code] = {
                        "description": response_details["description"],
                        "schema": resolved_schema,
                    }

                functions.append(function)

        return functions

    # openapi.yamlを関数定義に変換する
    def get(self) -> list:
        return self._convert_to_functions(self.openapi_definition)
