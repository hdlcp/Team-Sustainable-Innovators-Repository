# adapters/swagger_config.py
from flask import request 
from flasgger import Swagger

def setup_swagger(app):
    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": 'apispec',
                "route": '/apispec.json',
                "rule_filter": lambda rule: True,  # Include all routes
                "model_filter": lambda tag: True,  # Include all models
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/swagger/"
    }

    swagger_template = {
        "swagger": "2.0",
        "info": {
            "title": "SNAKING LEARNING",
            "description": "API documentation",
            "version": "1.0.0"
        },
        "host": "",
        "basePath": "/",
        "schemes": ["http", "https"],
        "securityDefinitions": {
            "JWT": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header",
                "description": "Enter 'Bearer <token>' to access secured endpoints",
                "scheme" : "bearer",
                "bearerFormat" : "JWT",
            }
        },
        "security": [
            {
                "JWT": []
            }
        ]
    }

    Swagger(app, config=swagger_config, template=swagger_template)
