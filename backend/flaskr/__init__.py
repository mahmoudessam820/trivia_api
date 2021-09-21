#----------------------------------------------------------------#
# Imports
#----------------------------------------------------------------#
import os
from flask import (Flask, request, abort, jsonify)
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

#-----------------------------------------------------------------#
# Paginate questions
#-----------------------------------------------------------------#

# Function to paginate questions
QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
  page_count = request.args.get('page', 1, type=int)
  start = (page_count - 1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE
  questions = [question.format() for question in selection]
  current_question = questions[start:end]

  return current_question

#----------------------------------------------------------------#
# Create app configure
#----------------------------------------------------------------#

def create_app(test_config=None):
  app = Flask(__name__)
  setup_db(app)

#----------------------------------------------------------------#
# Setup CORS
#----------------------------------------------------------------#

  # Set up CORS. Allow '*' for origins.
  CORS(app, resources={"/": {"origins":"*"}})
  # Use the after_request decorator to set Access-Control-Allow
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PUT, PATCH, DELETE, OPTIONS')
    return response

#----------------------------------------------------------------#
# API
#----------------------------------------------------------------#

  @app.route('/categories', methods=['GET'])
  def get_all_categories():
    CATEGORIES_PER_PAGE = 10
    pagination_categories = request.args.get('page', 1, type=int)
    start = (pagination_categories - 1) * CATEGORIES_PER_PAGE # result -> 0
    end = start + CATEGORIES_PER_PAGE # result -> 10

    categories = Category.query.all()
    formtted_catogories = [category.format() for category in categories]
    total_categories = len(formtted_catogories)

    # 404 if there is no categories 🥺
    if len(formtted_catogories) == 0:
      abort(404) 
    else:
      return jsonify({
        "Success": True,
        "Categories": formtted_catogories[start:end],
        "Total categories": total_categories,
        "Status": '😊' 
      }), 200 

  @app.route('/questions', methods=['GET']) 
  def get_all_questions():
    QUESTIONS_PER_PAGE = 10
    paginate_questions = request.args.get('page', 1, type=int)
    start = (paginate_questions - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    
    # Questions
    questions = Question.query.all()
    formated_questions = [question.format() for question in questions]
    total_questions = len(formated_questions)

    # Categories
    categories = Category.query.all()
    formated_categories = [category.format() for category in categories]
    tolal_categories = len(formated_categories)

    # 404 if there is no questions and categories 🥺
    if len(formated_questions) == 0 and len(formated_categories) == 0:
      abort(404)
    else:
      return jsonify({
        "Success": True,
        "Questions": formated_questions[start:end],
        "Total Questions": total_questions,
        "Categories": formated_categories[start:end],
        "Total Categories": tolal_categories,
        "Status": '😊'
      }), 200

  @app.route('/questions/<int:id>', methods=['DELETE'])
  def delete_one_question(id):
    try:
      del_one_qust = Question.query.filter_by(id=id).one_or_none()

      if del_one_qust is None:
        abort(404) # 🥺
      else:
        del_one_qust.delete()
        return jsonify({
          "Success": True,
          "Delete": id,
          "Status": '😊'
        }), 200
    except Unprocessable:  # 😵‍💫
      abort(422)

  @app.route('/question', methods=["POST"])
  def add_new_question():
    # load data from body
    new_question = request.get_json() 

    if len(new_question) == 0:
      abort(500)

    try:
      Question(
            question=new_question['question'], 
            answer=new_question['answer'], 
            difficulty=new_question['difficulty'], 
            category=new_question['category']
      ).insert()

      selection = Question.query.order_by(Question.id).all()
      currently_questions = paginate_questions(request, selection)

      return jsonify({
        'Success': True,
        'Questions': new_question,
        'Currently questions': currently_questions,
        'Total questions': len(Question.query.all()),
        'Message': 'Sucessfully posted questions 😊',
        'Status': '😊'
      })
    except Unprocessable: # 😵‍💫
      abort(422)

  @app.route('/search', methods=["POST"])
  def search():
    search_term = request.get_json()['searchTerm']
    search_data = Question.query.filter(Question.question.ilike(f'%{search_term}%'))

    return jsonify({
      "Question": [ques.format() for ques in search_data],
      "Current category": None
    })

  @app.route('/categories/<int:category_id>/questions', methods=["GET"])
  def get_question_by_category(category_id):
    all_questions_by_category = Question.query.filter(Question.category==category_id).all()
    format_questions = [question.format() for question in all_questions_by_category]

    if format_questions == 0:
      abort(404)

    return jsonify({
      "Success": True,
      "Questions": format_questions,
      "Total Questions": len(format_questions),
      "Current Question": category_id,
      "Status": '😊' 
    }), 200

  @app.route('/quizzes', methods=["POST"])
  def play_quizzes():
    quiz_category = int(request.get_json()['quiz_category']['id'])
    previous_questions = request.get_json()['previous_questions'] 
    questions_list = [1, 2, 3, 4, 5, 6]

    if quiz_category not in questions_list:
      unique_questions = Question.query.all()
    else:
      unique_questions = Question.query.filter_by(category=quiz_category).filter(Question.id.notin_(previous_questions)).all()

    if len(unique_questions) > 0:
      return jsonify({
        "Success": True,
        "Question": random.choice([question.format() for question in unique_questions]),
        "Category_": quiz_category,
        "Previous":  [unique.question for unique in unique_questions],
        "Status": '😊' 
      }), 200
    else:
      return jsonify({
        "Success": True,
        "Question": None 
      })

#----------------------------------------------------------------#
# Error handlers
#----------------------------------------------------------------#

  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422

  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "bad request"
    }), 400

  return app