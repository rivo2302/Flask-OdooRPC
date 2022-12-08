list_specs = {
    "tags": ["Product"],
    "description": "Get list of product items",
    "parameters": [
        {
            "in": "header",
            "name": "access-token",
            "type": "string",
            "required": True,
        }
    ],
    "definitions": {
        "product": {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "name": {"type": "string"},
                "description": {"type": "string"},
                "category_id": {"type": "integer"},
                "img_url": {"type": "string"},
                "qty_available": {"type": "integer"},
                "default_code": {"type": "string"},
            },
        }
    },
    "responses": {
        "200": {
            "description": " A list of categories items",
            "schema": {
                "type": "array",
                "items": {"$ref": "#/definitions/product"},
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
    "tags": ["Product"],
    "description": "Get detailed product item",
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
        "product": {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "name": {"type": "string"},
                "description": {"type": "string"},
                "category_id": {"type": "integer"},
                "img_url": {"type": "string"},
                "qty_available": {"type": "integer"},
                "default_code": {"type": "string"},
            },
        },
    },
    "responses": {
        200: {
            "description": "A product item",
            "schema": {"$ref": "#/definitions/product"},
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
            "description": "Product not found",
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
