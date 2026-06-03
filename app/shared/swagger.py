from flask import Blueprint, jsonify, render_template_string
from app.schema.employee import (
    EmployeeCreateSchema,
    EmployeeUpdateSchema,
    EmployeeResponseSchema,
    EmployeeResponseWrapperSchema,
    EmployeeListResponseWrapperSchema,
    EmployeePaginatedListResponseWrapperSchema,
    PaginatedMetaSchema,
    ApiResponseSchema
)

# Blueprint for Swagger UI and OpenAPI documentation
swagger_bp = Blueprint("swagger", __name__)

def resolve_pydantic_refs(spec_dict):
    """Recursively extract all Pydantic v2 nested definitions from $defs,
    move them into components.schemas, and rewrite refs to standard OpenAPI format.
    """
    schemas = spec_dict.setdefault("components", {}).setdefault("schemas", {})
    
    # 1. First, find all nested $defs across all registered schemas
    all_defs = {}
    for schema_name, schema in list(schemas.items()):
        if "$defs" in schema:
            all_defs.update(schema["$defs"])
            del schema["$defs"] # Remove local defs
            
    # 2. Add these nested defs to the global schemas registry
    for def_name, def_schema in all_defs.items():
        if def_name not in schemas:
            schemas[def_name] = def_schema

    # 3. Recursively replace any reference to "#/$defs/X" with "#/components/schemas/X"
    def rewrite_refs(node):
        if isinstance(node, dict):
            if "$ref" in node and isinstance(node["$ref"], str) and node["$ref"].startswith("#/$defs/"):
                ref_name = node["$ref"].split("/")[-1]
                node["$ref"] = f"#/components/schemas/{ref_name}"
            for val in node.values():
                rewrite_refs(val)
        elif isinstance(node, list):
            for item in node:
                rewrite_refs(item)

    rewrite_refs(spec_dict)

@swagger_bp.route("/openapi.json")
def get_openapi_json():
    """Dynamically build an OpenAPI 3.0.3 specification by extracting JSON schemas from Pydantic models."""
    openapi_spec = {
        "openapi": "3.0.3",
        "info": {
            "title": "Employee Management API",
            "version": "v1",
            "description": "A pure, lightweight Flask and Pydantic-based Employee Management System. Formatted with dependency injection and a FastAPI-like endpoint schema validation model."
        },
        "paths": {
            "/employees/": {
                "get": {
                    "summary": "Retrieve list of all employees",
                    "description": "Fetches all registered employee records with optional filtering, sorting, and pagination.",
                    "parameters": [
                        {
                            "name": "page",
                            "in": "query",
                            "schema": {"type": "integer", "default": 1},
                            "description": "The page number to retrieve (defaults to 1)."
                        },
                        {
                            "name": "limit",
                            "in": "query",
                            "schema": {"type": "integer", "default": 10},
                            "description": "The number of records per page (defaults to 10)."
                        },
                        {
                            "name": "sort",
                            "in": "query",
                            "schema": {"type": "string"},
                            "description": "Comma-separated sorting fields (e.g. 'name:asc,email:desc' or '-date_joined')."
                        },
                        {
                            "name": "search",
                            "in": "query",
                            "schema": {"type": "string"},
                            "description": "Global search term matched against name, email, department/designation, and date joined."
                        },
                        {
                            "name": "name",
                            "in": "query",
                            "schema": {"type": "string"},
                            "description": "Filter by employee name (partial match)."
                        },
                        {
                            "name": "email",
                            "in": "query",
                            "schema": {"type": "string"},
                            "description": "Filter by employee email (partial match)."
                        },
                        {
                            "name": "designation",
                            "in": "query",
                            "schema": {"type": "string"},
                            "description": "Filter by employee department/designation (partial match)."
                        },
                        {
                            "name": "join_date",
                            "in": "query",
                            "schema": {"type": "string", "format": "date"},
                            "description": "Filter by exact join date (YYYY-MM-DD)."
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Successful retrieval of employee records list.",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/EmployeePaginatedListResponseWrapper"
                                    }
                                }
                            }
                        }
                    }
                },
                "post": {
                    "summary": "Add a new employee",
                    "description": "Validates the request parameters using Pydantic, ensures email uniqueness, and registers the employee.",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/EmployeeCreate"
                                }
                            }
                        }
                    },
                    "responses": {
                        "201": {
                            "description": "Employee record successfully registered.",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/EmployeeResponseWrapper"
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "/employees/{id}": {
                "get": {
                    "summary": "Retrieve details of a specific employee",
                    "parameters": [
                        {
                            "name": "id",
                            "in": "path",
                            "required": True,
                            "schema": {
                                "type": "integer"
                            },
                            "description": "The unique identifier of the employee."
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Details of the requested employee.",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/EmployeeResponseWrapper"
                                    }
                                }
                            }
                        }
                    }
                },
                "patch": {
                    "summary": "Update an existing employee's information",
                    "parameters": [
                        {
                            "name": "id",
                            "in": "path",
                            "required": True,
                            "schema": {
                                "type": "integer"
                            },
                            "description": "The unique identifier of the employee."
                        }
                    ],
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/EmployeeUpdate"
                                }
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "Employee updated successfully.",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/EmployeeResponseWrapper"
                                    }
                                }
                            }
                        }
                    }
                },
                "delete": {
                    "summary": "Remove an employee from the system",
                    "parameters": [
                        {
                            "name": "id",
                            "in": "path",
                            "required": True,
                            "schema": {
                                "type": "integer"
                            },
                            "description": "The unique identifier of the employee."
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Employee successfully removed.",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/ApiResponse"
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        "components": {
            "schemas": {
                "EmployeeCreate": EmployeeCreateSchema.model_json_schema(),
                "EmployeeUpdate": EmployeeUpdateSchema.model_json_schema(),
                "EmployeeResponse": EmployeeResponseSchema.model_json_schema(),
                "EmployeeResponseWrapper": EmployeeResponseWrapperSchema.model_json_schema(),
                "EmployeeListResponseWrapper": EmployeeListResponseWrapperSchema.model_json_schema(),
                "PaginatedMeta": PaginatedMetaSchema.model_json_schema(),
                "EmployeePaginatedListResponseWrapper": EmployeePaginatedListResponseWrapperSchema.model_json_schema(),
                "ApiResponse": ApiResponseSchema.model_json_schema()
            }
        }
    }
    
    # Resolve Pydantic nested reference schemas ($defs) into global OpenAPI component schemas
    resolve_pydantic_refs(openapi_spec)
    
    return jsonify(openapi_spec)

@swagger_bp.route("/swagger-ui")
def swagger_ui():
    """Serve a standard self-contained Swagger UI page loading openapi.json."""
    swagger_ui_html = """
    <!DOCTYPE html>
    <html lang="en">
      <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <title>Employee Management API - Swagger UI</title>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css" />
      </head>
      <body>
        <div id="swagger-ui"></div>
        <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js" charset="UTF-8"></script>
        <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-standalone-preset.js" charset="UTF-8"></script>
        <script>
          window.onload = () => {
            window.ui = SwaggerUIBundle({
              url: '/openapi.json',
              dom_id: '#swagger-ui',
              deepLinking: true,
              presets: [
                SwaggerUIBundle.presets.apis,
                SwaggerUIStandalonePreset
              ],
              layout: "BaseLayout"
            });
          };
        </script>
      </body>
    </html>
    """
    return render_template_string(swagger_ui_html)
