from flask import Flask
from flask import jsonify, render_template, send_from_directory
from apiflask import Schema, fields
from apispec import APISpec
from apispec_webframeworks.flask import FlaskPlugin

from apispec.ext.marshmallow import MarshmallowPlugin


app = Flask(__name__)



@app.route('/')
def hello():
    return "Building started"

spec = APISpec(
    title = 'Flask-api-swagger-doc',
    version='1.0.0',
    openapi_version='3.0.2',
    plugins=[FlaskPlugin(), MarshmallowPlugin()]
)

@app.route('/api/swagger.json')
def create_swagger_spec():
    return jsonify(spec.to_dict())



class ToDoResponseSchema(Schema):
    id = fields.Integer()
    title = fields.String()
    status = fields.Boolean()

class ToDoListResponseSchema(Schema):
    todo_list = fields.List(fields.Nested(ToDoResponseSchema))

@app.route('/todo')
def todo():
    """Get list of Todo
        ---
        get: 
            description: Get list of Todos
            responses:
                200:
                    description : return of todo List
                    content:
                        application/json:
                            Schema: TodoListResponseSchema

    """
    dummy_data = [{
        'id': 1,
        'title': 'Finished this task',
        'status': False
    },
    {
        'id': 2,
        'title': 'Finished this task',
        'status': True 
    },
    {
        'id': 3,
        'title': 'Finished that task',
        'status': False
    }]

    return ToDoListResponseSchema().dump({'todo_list': dummy_data})

with app.test_request_context():
    spec.path(view=todo)

@app.route('/docs')
@app.route('/docs/<path:path>')
def swagger_docs(path=None):
    if not path or path == '/index.html':
        return render_template('index.html', base_url='/docs')
    else:
        return send_from_directory('./swagger/static', path)

if __name__ == "__main__":
    app.run(debug=True)