from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

# Initialize app
app = Flask(__name__)
CORS(app)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Models
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(255), nullable=False)
    options = db.Column(db.PickleType, nullable=False)  # List of options
    answer = db.Column(db.String(255), nullable=False)  # Correct answer

# Initialize database
def setup_database():
    db.create_all()
    if not Question.query.first():
        seed_data()

def seed_data():
    questions = [
        {
            "question": "What is the capital of France?",
            "options": ["Paris", "London", "Berlin", "Madrid"],
            "answer": "Paris"
        },
        {
            "question": "Which planet is known as the Red Planet?",
            "options": ["Earth", "Mars", "Jupiter", "Saturn"],
            "answer": "Mars"
        },
        {
            "question": "Who wrote 'Romeo and Juliet'?",
            "options": ["Shakespeare", "Hemingway", "Tolstoy", "Dickens"],
            "answer": "Shakespeare"
        }
    ]

    for q in questions:
        question = Question(question=q["question"], options=q["options"], answer=q["answer"])
        db.session.add(question)
    db.session.commit()

# Routes
@app.route('/questions', methods=['GET'])
def get_questions():
    try:
        questions = Question.query.all()
        output = []

        for question in questions:
            output.append({
                'id': question.id,
                'question': question.question,
                'options': question.options
            })

        return jsonify(output), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/questions/<int:id>', methods=['POST'])
def check_answer(id):
    try:
        data = request.get_json()
        user_answer = data.get('answer')

        question = Question.query.get(id)
        if not question:
            return jsonify({'error': 'Question not found'}), 404

        is_correct = question.answer == user_answer

        return jsonify({'is_correct': is_correct}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/random', methods=['GET'])
def get_random_question():
    try:
        questions = Question.query.all()
        if not questions:
            return jsonify({'error': 'No questions available'}), 404

        question = random.choice(questions)
        return jsonify({
            'id': question.id,
            'question': question.question,
            'options': question.options
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    setup_database()
    app.run(debug=True)
