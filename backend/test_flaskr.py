import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://postgres:postgres@{}/{}".format('localhost:5432', self.database_name)
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

    """
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_categories(self):
        """" gets categories using /categories endpoint"""
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['categories']))

    def test_create_category(self):
        """creates a category"""

        new_type = 'new type'
        #1) request creation with valid data 
        new_category = {'type':new_type }
        res = self.client().post('/categories', json=new_category)
        data = json.loads(res.data)
        #get the last inserted category
        inserted_category = Category.query.order_by(self.db.desc(Category.id)).first()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['created'],inserted_category.id)
        self.assertEqual(inserted_category.type , new_type)
        self.assertTrue(data['total_categories'])

        #2) request creation with no type provided

        res = self.client().post('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable Entity')

    def test_delete_category(self):
        """request a valid category deletion"""
        category = Category.query.order_by(self.db.desc(Category.id)).first()
        self.assertNotEqual(category, None)
        category_id =category.id
        res = self.client().delete('/categories/'+str(category_id))
        data = json.loads(res.data)
        category = Category.query.get(category_id)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], category_id)
        self.assertTrue(data['total_categories'])
        self.assertEqual(category, None)
        
    def test_delete_category422(self):
        """request a delete with unknown id"""
        res = self.client().delete('/categories/12123')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable Entity')
    
    def test_get_questions_no_page(self):
        """" gets questions using /questions endpoint without a page argument"""
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
        self.assertTrue(len(data['categories']))
    
    def test_get_questions_valid_page(self):
        """" gets questions using /questions endpoint without a page argument"""
        res = self.client().get('/questions?page=2')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
        self.assertTrue(len(data['categories']))
    
    def test_get_questions404(self):
        """requests a page beyond the range of pages"""
        res = self.client().get('/questions?page=10000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not Found')

    def test_create_question(self):
        """Apply MCDC on the data required to create a question"""

        #1) request creation with valid data 
        new_question = {'question':"new question" , 'answer':'answer' , 'difficulty':1, 'category':1}
        res = self.client().post('/questions', json=new_question)
        data = json.loads(res.data)
        #get the last inserted question 
        inserted_question = Question.query.order_by(self.db.desc(Question.id)).first()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['created'], inserted_question.id)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))

        #2) request creation with no question provided
        new_question = {'answer':'answer' , 'difficulty':1, 'category':1}
        res = self.client().post('/questions', json=new_question)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable Entity')

        #3) request creation with no answer provided
        new_question = {'question':'new question' , 'difficulty':1, 'category':1}
        res = self.client().post('/questions', json=new_question)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable Entity')

        #4) request creation with no difficulty provided
        new_question = {'answer':'answer' , 'question':'new question', 'category':1}
        res = self.client().post('/questions', json=new_question)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable Entity')

        #5) request creation with no category provided
        new_question = {'answer':'answer' , 'difficulty':1, 'question':'new question'}
        res = self.client().post('/questions', json=new_question)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable Entity')
        pass
    
    def test_delete_question(self):
        """request a valid question deletion"""
        question = Question.query.order_by(self.db.desc(Question.id)).first()
        self.assertNotEqual(question, None)
        question_id =question.id
        res = self.client().delete('/questions/'+str(question_id))
        data = json.loads(res.data)
        question = Question.query.get(question_id)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], question_id)
        self.assertTrue(data['total_questions'])
        self.assertEqual(question, None)
        
    def test_delete_question422(self):
        """request a delete with unknown id"""
        res = self.client().delete('/questions/12233')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable Entity')
    

    def test_search_question_with_results(self):
        """searches questions with existing results"""
        res = self.client().post('/questions', json={'searchTerm':'the'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        #ensures that no new question is created as they are handled in the same route
        is_created = False
        try:
            data['created']
            is_created = True
        except:
            pass
        self.assertEqual(is_created,False)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))

    def test_search_question_with_noresults(self):
        """searches questions with no results"""
        res = self.client().post('/questions', json={'searchTerm':'dsfldjsfkrwekrljfdsfjk'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        #ensures that no new question is created as they are handled in the same route
        is_created = False
        try:
            data['created']
            is_created = True
        except:
            pass
        self.assertEqual(is_created,False)
        self.assertEqual(data['total_questions'],0)
        self.assertEqual(len(data['questions']),0)

    def test_patch_question405(self):
        '''send patch request to questions'''
        res = self.client().patch('/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Method Not Allowed')


    def test_get_questions_by_category(self):
        """" gets questions by category """
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
        self.assertEqual(data['current_category'],1)

    def test_get_questions_by_category404(self):
        """" gets questions by invalid category """
        res = self.client().get('/categories/10000/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not Found')

    def test_post_questions_by_category405(self):
        '''sends post request to categories/1/questions'''
        res = self.client().post('/categories/1/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Method Not Allowed')

    
    def test_post_quiz_questions_allCategories(self):
        """" gets quiz questions with category = 0 """

        #get the total number of questions
        res = self.client().get('/questions')
        data = json.loads(res.data)
        total_number =  data['total_questions']

        #request with previous questions as empty list
        res = self.client().post('/quizzes', json={'previous_questions':[] , 'quiz_category':{'id':0}})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_questions'] , total_number)
        self.assertTrue(data['question'])

        #request with a previous question
        question = Question.query.first()
        res = self.client().post('/quizzes', json={'previous_questions':[question.id] , 'quiz_category':{'id':0}})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_questions'] , total_number-1)
        self.assertTrue(data['question'])
    
    def test_post_quiz_questions_byCategory(self):
        """" gets quiz questions with category = 1"""

        #get the total number of questions
        res = self.client().get('/questions')
        data = json.loads(res.data)
        total_number =  data['total_questions']

        res = self.client().post('/quizzes', json={'previous_questions':[] , 'quiz_category':{'id':1}})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertNotEqual(data['total_questions'] , total_number)
        self.assertTrue(data['question'])
        
    def test_post_quiz_questions_byCategory400(self):
        """" send a request with no data """

        res = self.client().post('/quizzes')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request')
    
    def test_get_quiz_questions405(self):
        '''sends get request to /quizzes'''
        res = self.client().get('/quizzes')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Method Not Allowed')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()