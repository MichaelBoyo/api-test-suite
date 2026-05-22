import jsonschema
from jsonschema import validate

class OpenAPIValidator:
    def __init__(self, spec):
        self.spec = spec
        self._build_schema_map()

    def _build_schema_map(self):
        self.schemas = self.spec.get("definitions", {})
        self.path_schemas = {}
        for path, methods in self.spec.get("paths", {}).items():
            for method, details in methods.items():
                responses = details.get("responses", {})
                for code, resp in responses.items():
                    if "schema" in resp:
                        ref = resp["schema"].get("$ref")
                        if ref:
                            schema_name = ref.split("/")[-1]
                            schema = self.schemas.get(schema_name)
                        else:
                            schema = resp["schema"]
                        self.path_schemas[(path, method.upper(), code)] = schema

    def validate_response(self, path, method, status_code, body):
        key = (path, method.upper(), str(status_code))
        schema = self.path_schemas.get(key)
        if not schema:
            return
        try:
            validate(instance=body, schema=schema)
        except jsonschema.ValidationError as e:
            raise AssertionError(f"Response does not match schema for {method} {path} ({status_code}): {e.message}")
