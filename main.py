from crypt import methods
import logging
from flask import Flask, abort, request, render_template
from google.api_core.gapic_v1 import method
from werkzeug.utils import redirect
import ds


app = Flask(__name__)
logging.getLogger().setLevel(logging.DEBUG)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/todo')
def todo():
    data = ds.get_all()
    message = "Hi, This is ToDoList"
    return render_template('todo.html',
                    message=message,
                    data=data)

@app.route('/todo/check/<key_id>', methods=['PUT', 'DELETE'])
def check(key_id=None):
    if request.method == 'PUT':
        entity = ds.get_by_id(key_id)
        if not entity:
            abort(404)
            return entity
    
        entity['check'] = "1"
        entity = ds.update(entity)
        return entity
        
    elif request.method == 'DELETE':
        ds.delete(key_id)
        return '', 204

@app.route('/todo/admin')
def admin():
    data = ds.get_all()
    message = "ToDoList admin"
    return render_template('admin.html',
                    message=message,
                    data=data)

@app.route('/todo/add', methods=['POST'])
def add():
    addtodo = request.form.get('addtodo', '')
    if addtodo == '':
        return redirect('/todo/admin')
    things = addtodo
    check = "0"
    entity = ds.insert(things, check)
    return entity, 201



if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)