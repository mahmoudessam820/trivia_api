#----------------------------------------------------------------#
# Imports
#----------------------------------------------------------------#
import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category

#----------------------------------------------------------------#
# Unittest Setup
#----------------------------------------------------------------#

class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.user_name = 'postgres'
        self.password = 1234
        self.host = 'localhost:5432'
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}:{}@{}/{}".format(self.user_name, self.password, self.host, self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

#----------------------------------------------------------------#
# Test Cases
#----------------------------------------------------------------#

    def test_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['Success'], True)
        self.assertEqual(len(data['Categories']), 6)

    def test_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['Success'], True)
        self.assertEqual(data['Total Questions'], 67)
        self.assertEqual(data['Total Categories'], 6)

    def test_questions_with_pagination(self):
        res = self.client().get('questions?page=1')
        data = json.loads(res.data)

        self.assertEqual(len(data['Questions']), 10)

    def test_search_term(self):
        body = {"searchTerm": "What is API?"}
        res = self.client().post('/search', json=body)
        data = json.loads(res.data)

        self.assertEqual(len(data['Question']), 1) 

    def test_create_new_question(self):
        data = {
            "question": "What is DNS?",
            "answer": "Mahmoud",
            "category": 1,
            "difficulty": 3 
        }
        res = self.client().post('/question', json=data)
        self.assertEqual(res.status_code, 200, 'POST question is not succesful!')

    def test_question_by_category(self):
        res = self.client().get('/categories/2/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200, 'Response status is not 200')
        self.assertTrue(data['Questions'])

    def test_quiz(self):
        body = {
            "quiz_category": {
                "id": 2
            },
            "previous_questions": []
        }
        res = self.client().post('/quizzes', json=body)
        data = json.loads(res.data)

        self.assertEqual(data['Category_'], 2, 'Category do not match')

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()