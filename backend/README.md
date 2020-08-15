# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 


## API Reference

### Getting Started
- Base URL: this app is hosted locally at `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration. 
- Authentication: no authentication required. 

### Error Handling
Errors are returned as JSON objects:
```
{
    "success": False, 
    "error": 404,
    "message": "Not Found"
}
```
returned error codes:
- 400: Bad Request
- 404: Not Found
- 422: Unprocessable Entity
- 500: Internal Server Error (rare)

### Endpoints 
### GET / 
- General:
    - Returns success value, available categories as a dictionary along with their total number, available questions as a list along with their total number
- Sample: `curl http://127.0.0.1:5000`

``` 
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "questions": [
    {
      "answer": "Alexander Fleming", 
      "category": 1, 
      "difficulty": 3, 
      "id": 21, 
      "question": "Who discovered penicillin?"
    }, 
    {
      "answer": "Blood", 
      "category": 1, 
      "difficulty": 4, 
      "id": 22, 
      "question": "Hematology is a branch of medicine involving the study of what?"
    }
  ], 
  "success": true, 
  "total_categories": 6, 
  "total_questions": 2
}
```
#### GET /categories
- General:
    - Returns  categories as a dictionary and success value
- Sample: `curl http://127.0.0.1:5000/categories`

``` 
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "success": true
}
```

#### POST /categories
- General:
    - Creates a new category using the submitted type. Returns the id of the created category , success value and total categories.
- `curl http://127.0.0.1:5000/categories -X POST -H "Content-Type: application/json" -d '{"type":"new Category"}'`
```
{
  "created": 7,
  "success": true,
  "total_categories": 7
}
```
#### DELETE /categories/{category_id}
- General:
    - Deletes the category of the given ID if it exists. Returns the id of the deleted category , success value and total categories 
- `curl -X DELETE http://127.0.0.1:5000/categories/8`
```
{
  "deleted": 8,
  "success": true,
  "total_categories": 6
}
```
#### GET /questions
- General:
    - Returns available categories as dictionary ,a list of question objects for the given page number, success value, and total number of questions.
    - Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1. 
- Sample: `curl http://127.0.0.1:5000/questions?page=2`

``` {
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "questions": [
    {
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    },
    {
      "answer": "Escher",
      "category": 2,
      "difficulty": 1,
      "id": 16,
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    },
    {
      "answer": "Mona Lisa",
      "category": 2,
      "difficulty": 3,
      "id": 17,
      "question": "La Giaconda is better known as what?"
    },
    {
      "answer": "One",
      "category": 2,
      "difficulty": 4,
      "id": 18,
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    },
    {
      "answer": "Jackson Pollock",
      "category": 2,
      "difficulty": 2,
      "id": 19,
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    },
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    },
    {
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    },
    {
      "answer": "Blood",
      "category": 1,
      "difficulty": 4,
      "id": 22,
      "question": "Hematology is a branch of medicine involving the study of what?"
    },
    {
      "answer": "Scarab",
      "category": 4,
      "difficulty": 4,
      "id": 23,
      "question": "Which dung beetle was worshipped by the ancient Egyptians?"
    }
  ],
  "success": true,
  "total_questions": 19
}
```

#### POST /questions
- General:
    - Creates a new question using the submitted question, answer,difficulty and category. Returns the id of the created question, success value, total questionss, and question list based on current page .
	- `curl http://127.0.0.1:5000/questions?page=2-X POST -H "Content-Type: application/json" -d '{"question":"New question", "answer":"example answer", "category":"1" , "difficulty":"2"}'`
```
{
  "created": 24,
  "questions": [
    {
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    },
    {
      "answer": "Escher",
      "category": 2,
      "difficulty": 1,
      "id": 16,
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    },
    {
      "answer": "Mona Lisa",
      "category": 2,
      "difficulty": 3,
      "id": 17,
      "question": "La Giaconda is better known as what?"
    },
    {
      "answer": "One",
      "category": 2,
      "difficulty": 4,
      "id": 18,
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    },
    {
      "answer": "Jackson Pollock",
      "category": 2,
      "difficulty": 2,
      "id": 19,
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    },
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    },
    {
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    },
    {
      "answer": "Blood",
      "category": 1,
      "difficulty": 4,
      "id": 22,
      "question": "Hematology is a branch of medicine involving the study of what?"
    },
    {
      "answer": "Scarab",
      "category": 4,
      "difficulty": 4,
      "id": 23,
      "question": "Which dung beetle was worshipped by the ancient Egyptians?"
    },
    {
      "answer": "example answer",
      "category": 1,
      "difficulty": 2,
      "id": 24,
      "question": "New question"
    }
  ],
  "success": true,
  "total_questions": 20
}
```
- Special usage : 
	given a search term, returns the questions matching the string (case insensitive), success value and the total number of questions matching the search term.
	- `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"searchTerm":"title"}'`
```
{
  "questions": [
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }
  ],
  "success": true,
  "total_questions": 2
}
```
#### DELETE /questions/{book_id}
- General:
    - Deletes the question of the given ID if it exists. Returns the id of the deleted question, success value and total questions.
- `curl -X DELETE http://127.0.0.1:5000/questions/26`
```
{
  "deleted": 26,
  "success": true,
  "total_questions": 21
}
```
#### GET /categories/{category_id}/questions
- General:
    - gets all questions belonging to the given category, returns the current category, a list of the questions paginated , success value and total number of questions in the category. if no questions found the request is still processed and returns a total number of 0 and an empty questions list
- `curl http://127.0.0.1:5000/categories/6/questions`
```
{
  "current_category": 6,
  "questions": [
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }
  ],
  "success": true,
  "total_questions": 2
}
```
#### POST /quizzes
- General:
    - takes a  list of previous_questions and a quiz_category and returns a random question belonging to the given category and is not in the previous questions list, total number of questions left(including the returned question) and success value. if category is zero, the request queries all the questions that are not in the previous questions list.
 
 - Example1 :
	- `curl http://127.0.0.1:5000/quizzes -H "Content-Type: application/json" -d '{"previous_questions":[], "quiz_category":{"id":"1"}}`
```
{
  "question": {
    "answer": "Blood",
    "category": 1,
    "difficulty": 4,
    "id": 22,
    "question": "Hematology is a branch of medicine involving the study of what?"
  },
  "success": true,
  "total_questions": 5
}
```
- Example2:
	- `curl http://127.0.0.1:5000/quizzes -H "Content-Type: application/json" -d '{"previous_questions":[20,21,24], "quiz_category":{"id":"1"}}`
```
{
  "question": {
    "answer": "Blood",
    "category": 1,
    "difficulty": 4,
    "id": 22,
    "question": "Hematology is a branch of medicine involving the study of what?"
  },
  "success": true,
  "total_questions": 2
}
```
#### Author:
<sup>Alaa Sayed

## Acknowledgements 
The awesome team at Udacity and all of the students, soon to be full stack extraordinaires!
```


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```