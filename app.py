# pip install flask flask_sqlalchemy
#python app.py
#pip freeze > requirements.txt

from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Veritabanı yapılandırması
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Todo modeli
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)
    done = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {"id": self.id, "task": self.task, "done": self.done}

# Veritabanını oluştur
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')
# GET /todos
@app.route('/todos', methods=['GET'])
def get_todos():
    todos = Todo.query.all()
    return jsonify([todo.to_dict() for todo in todos])

# GET /todos/<id>
@app.route('/todos/<int:todo_id>', methods=['GET'])
def get_todo(todo_id):
    todo = Todo.query.get(todo_id)
    if todo:
        return jsonify(todo.to_dict())
    else:
        return jsonify({"error": "Todo bulunamadı"}), 404

# POST /todos
@app.route('/todos', methods=['POST'])
def create_todo():
    data = request.get_json()
    new_todo = Todo(task=data['task'])
    db.session.add(new_todo)
    db.session.commit()
    return jsonify(new_todo.to_dict()), 201

# PUT /todos/<id>
@app.route('/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    todo = Todo.query.get(todo_id)
    if not todo:
        return jsonify({"error": "Todo bulunamadı"}), 404

    data = request.get_json()
    todo.task = data.get("task", todo.task)
    todo.done = data.get("done", todo.done)
    db.session.commit()
    return jsonify(todo.to_dict())

# DELETE /todos/<id>
@app.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    todo = Todo.query.get(todo_id)
    if not todo:
        return jsonify({"error": "Todo bulunamadı"}), 404

    db.session.delete(todo)
    db.session.commit()
    return jsonify({"message": "Silindi"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

