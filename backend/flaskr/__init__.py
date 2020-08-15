import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db , Question , Category
import random
#to handle generic exception
from werkzeug.exceptions import HTTPException

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10
def paginate_questions(request,selection):
  current_questions = []
  page = request.args.get('page',1,type=int)
  start = (page-1)*QUESTIONS_PER_PAGE 
  end = start + QUESTIONS_PER_PAGE
  questions = [question.format() for question in selection]
  current_questions = questions[start:end]
  return current_questions

#returns a dictionary of {id:type} for all available categories
def get_categories_dict(categories):
  categories_dict = {}
  for category in categories:
    categories_dict[category.id] = category.type
  return(categories_dict)


def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)

  cors = CORS(app, resources={r"/*": {"origins": "*"}})
  # CORS Headers 
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,DELETE')
    return response

  ''' create endpoint for API's root'''
  @app.route('/',methods=['GET'])
  def index():
    try: 
      questions = [question.format() for question in Question.query.order_by(Question.id).all()]
      categories =Category.query.order_by(Category.id).all()
      return jsonify({
            'success':True,
            'categories':get_categories_dict(categories),
            'total_categories':len(categories),
            'questions':questions,
            'total_questions':len(questions)
            })
    except:
      abort(500)
  '''
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories',methods=['GET'])
  def get_categories():
    categories = Category.query.order_by(Category.id).all()
    if(len(categories)==0):
      abort(404)
    return jsonify({
            'success':True,
            'categories':get_categories_dict(categories)
            })

  ''' add endpoint to create a new category '''
  @app.route('/categories',methods=['POST'])
  def create_categories():
    try:
      body = request.get_json()  
      category_type = body.get('type',None)
      if(category_type is None):
        abort(422)
      category = Category(type=category_type)
      category.insert()
      selection = Category.query.order_by(Category.id).all()
    
      return jsonify({
          'success':True,
          'created': category.id,
          'total_categories' : len(selection)
              })
    except :
      abort(422)

  '''added enpoint to delete a category'''
  @app.route('/categories/<int:category_id>',methods=['DELETE'])
  def delete_category(category_id):
    try:
      category = Category.query.get(category_id)
      if category is None:
        abort(404)
      category.delete()
      selection = Category.query.order_by(Category.id).all()
      return jsonify({
          'success':True,
          'deleted':category.id,
          'total_categories':len(selection)
          })
    except :
      abort(422)
  '''
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  why is the frontend requiring current_category on this request? this was so confusing
  specially that the todo mentions I should provide one
  '''
  
  @app.route('/questions',methods=['GET'])
  def get_questions():
    selection = Question.query.order_by(Question.id).all()
    current_questions = paginate_questions(request, selection)
    if(len(current_questions)==0):
      abort(404)
    categories = Category.query.order_by(Category.id).all()
    return jsonify({
            'success':True,
            'questions':current_questions,
            'total_questions' : len(selection),
            'categories' : get_categories_dict(categories),
            })
  
  '''
  Create an endpoint to DELETE question using a question ID. 
  '''
  @app.route('/questions/<int:question_id>',methods=['DELETE'])
  def delete_question(question_id):
    try:
      question = Question.query.get(question_id)
      if question is None:
        abort(404)
      question.delete()
      selection = Question.query.order_by(Question.id).all()
      return jsonify({
          'success':True,
          'deleted':question_id,
          'total_questions':len(selection)
          })
    except :
      abort(422)

  '''
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  the two requests are merged together
  '''
  @app.route('/questions',methods=['POST'])
  def create_search_question():
    body = request.get_json()  
    question = body.get('question',None)
    answer = body.get('answer',None)
    category = body.get('category',None)
    difficulty = body.get('difficulty',None)
    search = body.get('searchTerm',None)

    try:
      if search is not None:
        if(len(search) == 0 ):
          selection = Question.query.order_by(Question.id).all()
        else:
          selection = Question.query.order_by(Question.id).filter(Question.question.ilike('%{}%'.format(search))).all()

        current_questions = paginate_questions(request, selection)
        return jsonify({
            'success':True,
            'questions':current_questions,
            'total_questions' : len(selection)
            })
      
      else:
        if(not(question and answer and category and difficulty)):
          abort(422)
        question_obj = Question(question=question ,answer=answer, category=category , difficulty=difficulty)
        question_obj.insert()  
        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, selection)
        return jsonify({
            'success':True,
            'created': question_obj.id,
            'questions':current_questions,
            'total_questions' : len(selection)
            })
    except Exception as e:
      print(e)
      abort(422)


  '''
  Create a GET endpoint to get questions based on category.  
  '''
  @app.route('/categories/<int:category_id>/questions',methods=['GET'])
  def get_questions_by_category(category_id):
    category = Category.query.get(category_id)
    if category is None :
      abort(404)
    
    selection = Question.query.order_by(Question.id).filter(Question.category == category_id ).all()
    current_questions = paginate_questions(request, selection)

    return jsonify({
            'success':True,
            'questions':current_questions,
            'total_questions' : len(selection),
            'current_category' : category_id
            })

  '''
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 
  '''
  @app.route('/quizzes', methods=['POST'])
  def get_quiz_question():
    body = request.get_json()
    print(body)
    try:
      previous_questions = body.get('previous_questions')

      #print(previous_questions)
      print(body)
      quiz_category = body.get('quiz_category')['id']
      
      
      if (previous_questions is None):
              abort(400)

      questions = []
      if quiz_category == 0 :
        questions = Question.query.filter(Question.id.notin_(previous_questions)).all()
      else:
        category = Category.query.get(quiz_category)
        if category is None:
          abort(404)
        questions = Question.query.filter(Question.id.notin_(previous_questions),Question.category == quiz_category).all()
      current_question = None
      if(len(questions)>0):
        index = random.randrange(0, len(questions))
        current_question = questions[index].format()
      return jsonify({
              'success':True,
              'question':current_question,
              'total_questions' : len(questions),
              })
    except Exception as e:
      print(e)
      abort(400)

  '''
  Create error handlers for all expected errors 
  including 404 and 422. 
  solution based on https://flask.palletsprojects.com/en/1.1.x/errorhandling/ examples
  '''
  @app.errorhandler(HTTPException)
  def handle_exception(e):
    return jsonify({
      "success": False, 
      "error": e.code,
      "message": e.name
      }), e.code
  
  return app

    