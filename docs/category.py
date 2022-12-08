category_specs = {
    "parameters": [],
    "definitions": {
{            "Category":
                "type" : "object",
                "properties":
                { "id":
                   { "type": "integer"},
                "name":
                   { "type": "string"},
                "image":
                    {"type": "string"}
                }
            }
    },
    "responses": {
        "200": {
            "description": " A list of categories",
            "schema": {
                "type": "array",
                "items": {"$ref": "#/definitions/Category"},
            },
            "examples": [
                {
                    "id": 1,
                    "name": "Category 1",
                    "image": "http://localhost:8000/uploads/images/1.jpg",
                },
                {
                    "id": 2,
                    "name": "Category 2",
                    "image": "http://localhost:8000/uploads/images/2.jpg",
                },
            ],
        }
    },
}
