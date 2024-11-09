from app import app, db
from db.models import User, Chat, Task
from flask import request, jsonify
import datetime
from config import Config


secret_key = Config.SECRET_KEY

@app.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()

    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')
    password = data.get('password')
    id = new_id()
    try:
        user = User(id=id, first_name=first_name, last_name=last_name, email=email, password=password)
        db.session.add(user)
        db.session.commit()

        return jsonify({'message': 'User created successfully!',
                        'user:': {
                            'id': user.id,
                            'first_name': user.first_name,
                            'last_name': user.last_name}}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 400




def new_id():
    max_id = db.session.query(db.func.max(User.id)).scalar()
    if max_id is None:
        return 1
    return max_id + 1