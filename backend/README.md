# API Reference 

## Getting Started
Base URL: At present this app con only be run locally and is not as a base URL yet. The backend app is hosted at the default, http://127.0.0.1:5000/, which is set as a proxy in the frontend configuration.
Authentication: this version of the application does not require authentication or API keys.
You can use in visual studio code extension Thunder client or postman to test the endpoints if you want. 

## Error Handling

Errors are returned as JSON objects in the following fromat:

```
{
  "error": 400,
  "message": "bad request",
  "success": false
}
{ 
  "error": 404,
  "message": "resource not found"
  "success": False
}
{ 
  "error": 422,
  "message": "unprocessable"
  "success": False
}

```

## The API will return three error type when request fail:

400: Bad Request 
404: Resource Not Found
422: Not Porcessable

## Endpoints
#### GET/categories

General:

Returns a list of categories objects value, and total number of categories
Returns are paginated in groups of 10


Smple: curl -X GET http://127.0.0.1:5000/categories

```
{
  "Categories": [
    {
      "id": 1,
      "type": "Science"
    },
    {
      "id": 2,
      "type": "Art"
    },
    {
      "id": 3,
      "type": "Geography"
    },
    {
      "id": 4,
      "type": "History"
    },
    {
      "id": 5,
      "type": "Entertainment"
    },
    {
      "id": 6,
      "type": "Sports"
    }
  ],
  "Status": "😊",
  "Success": true,
  "Total categories": 6
}

```

#### GET/questions

General:

Returns a list of questions objects value, and total number of questions
Returns are paginated in groups of 10

Smple: curl -X GET http://127.0.0.1:5000/questions

```
{
  "Categories": [
    {
      "id": 1,
      "type": "Science"
    },
    {
      "id": 2,
      "type": "Art"
    },
    {
      "id": 3,
      "type": "Geography"
    },
    {
      "id": 4,
      "type": "History"
    },
    {
      "id": 5,
      "type": "Entertainment"
    },
    {
      "id": 6,
      "type": "Sports"
    }
  ],
  "Questions": [
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
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
    },
    {
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    },
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
      "question": "Which Dutch graphic artist–initials M C was a creator of optical illusions?"
    }
  ],
  "Status": "😊",
  "Success": true,
  "Total Categories": 6,
  "Total Questions": 67
}

```

#### DELETE/questions

General:

DELETE question using a question ID.

Smple: curl -X DEL http://127.0.0.1:5000/questions/15

```
{
  "Delete": 15,
  "Status": "😊",
  "Success": true
}

```

#### POST/question

General:

POST a new question, which will require the question and answer text, category, and difficulty score.

Smple: curl -X POST http://127.0.0.1:5000/question

Exemple new question:

```

{
  "answer": "S7S",
  "category": 1,
  "difficulty": 3,
  "question": "How the internet work?"
}

```

The message after add new question:

```
{
  "Message": "Sucessfully posted questions 😊",
  "Questions": {
    "answer": "S7S",
    "category": 1,
    "difficulty": 3,
    "question": "How the internet work?"
  },
  "Status": "😊",
  "Success": true,
  "Total questions": 67
}
```

#### POST/search

General:

POST endpoint to get questions based on a search term. 

Smple: curl -X POST http://127.0.0.1:5000/search

Search body: 

```
{
    "searchTerm": "What is API?"
}

```

Response:

```
{
  "Current category": null,
  "Question": [
    {
      "answer": "Tito",
      "category": 1,
      "difficulty": 3,
      "id": 58,
      "question": "What Is API?"
    }
  ]
}
```

#### GET/questions/category

General:

Create a GET endpoint to get questions based on category.

Smple: curl -X GET http://127.0.0.1:5000/categories/2/questions


```
{
  "Current Question": 2,
  "Questions": [
    {
      "answer": "Escher",
      "category": 2,
      "difficulty": 1,
      "id": 16,
      "question": "Which Dutch graphic artist–initials M C was a creator of optical illusions?"
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
    }
  ],
  "Status": "😊",
  "Success": true,
  "Total Questions": 4
}

```

#### POST/quizzes

General:

Create a POST endpoint to get questions to play the quiz.

Smple: curl -X POST http://127.0.0.1:5000/quizzes

Quizze body:

```
{
    "quiz_category": {
        "id": 2
    },
    "previous_questions": []
}

```

Response:

```
{
  "Category_": 2,
  "Previous": [
    "Which Dutch graphic artist–initials M C was a creator of optical illusions?",
    "La Giaconda is better known as what?",
    "How many paintings did Van Gogh sell in his lifetime?",
    "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
  ],
  "Question": {
    "answer": "Jackson Pollock",
    "category": 2,
    "difficulty": 2,
    "id": 19,
    "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
  },
  "Status": "😊",
  "Success": true
}

```