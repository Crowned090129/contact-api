from flask import Flask, jsonify, redirect
from flask_restful import Api, MethodNotAllowed, NotFound
from flask_cors import CORS
from util.common import ENVIRONMENT, build_swagger_config_json
from resources.swaggerConfig import SwaggerConfig
from resources.contactResource import (
    ContactsGETResource, ContactGETResource, ContactPOSTResource, 
    ContactPUTResource, ContactDELETEResource
)
from flask_swagger_ui import get_swaggerui_blueprint

def start_backend():
    app = Flask(__name__)
    app.config['PROPAGATE_EXCEPTIONS'] = True

    # Initialize CORS
    CORS(app, resources={r"/swagger/*": {"origins": "*"}})

    env = ENVIRONMENT()
    api = Api(app, prefix=env.get_prefix(), catch_all_404s=True)
    
    # Configure Swagger
    build_swagger_config_json()
    swaggerui_blueprint = get_swaggerui_blueprint(
        env.get_prefix(),
        f'http://{env.get_domain()}:{env.get_port()}{env.get_prefix()}/swagger-config',
        config={
            'app_name': "Contact API",
            "layout": "BaseLayout",
            "docExpansion": "none"
        },
    )
    app.register_blueprint(swaggerui_blueprint, url_prefix=env.get_prefix())

    # Error Handlers
    @app.errorhandler(NotFound)
    def handle_not_found(e):
        return jsonify({"message": str(e)}), 404

    @app.errorhandler(MethodNotAllowed)
    def handle_method_not_allowed(e):
        return jsonify({"message": str(e)}), 405

    @app.route('/')
    def redirect_to_prefix():
        prefix = env.get_prefix()
        if prefix:
            return redirect(prefix)
        return jsonify({"message": "Welcome to the Contact API"})

    # Add Resources
    api.add_resource(SwaggerConfig, '/swagger-config')
    api.add_resource(ContactsGETResource, '/contacts')
    api.add_resource(ContactGETResource, '/contacts/<int:id>')
    api.add_resource(ContactPOSTResource, '/contacts')
    api.add_resource(ContactPUTResource, '/contacts/<int:id>')
    api.add_resource(ContactDELETEResource, '/contacts/<int:id>')

    return app

app = start_backend()
if __name__ == '__main__':
    try:
        app.run(debug=True)
    except Exception as e:
        print(f"Error running the application: {e}")
