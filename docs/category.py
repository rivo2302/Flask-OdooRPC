list_specs = {
    "tags": ["Category"],
    "description": "Get list of category items",
    "parameters": [
        {
            "in": "header",
            "name": "access-token",
            "type": "string",
            "required": True,
        }
    ],
    "definitions": {
        "Category": {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "name": {"type": "string"},
                "image": {"type": "string"},
            },
        }
    },
    "responses": {
        "200": {
            "description": " A list of categories items",
            "schema": {
                "type": "array",
                "items": {"$ref": "#/definitions/Category"},
            },
        },
        401: {
            "description": "Unauthorized",
            "schema": {
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                    }
                },
            },
        },
    },
}

detailed_specs = {
    "tags": ["Category"],
    "description": "Get detailed category item",
    "parameters": [
        {
            "in": "header",
            "name": "access-token",
            "type": "string",
            "required": True,
        },
        {
            "in": "path",
            "name": "id",
            "type": "integer",
            "required": True,
        },
    ],
    "definitions": {
        "Category": {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "name": {"type": "string"},
                "description": {"type": "string"},
            },
        },
    },
    "responses": {
        200: {
            "description": "A category item",
            "schema": {"$ref": "#/definitions/Category"},
        },
        401: {
            "description": "Unauthorized",
            "schema": {
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                    }
                },
            },
        },
        404: {
            "description": "Category not found",
            "schema": {
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                    }
                },
            },
        },
    },
}
