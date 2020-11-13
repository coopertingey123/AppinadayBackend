from flask import Flask, request, jsonify  
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS 
import os


app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "app.sqlite" )

db = SQLAlchemy(app)
ma = Marshmallow(app)
CORS(app)

class Question:
     def __init__(self, prompt, answer):
          self.prompt = prompt
          self.answer = answer
question_prompts = [
    "Do you like to Party?\n(a)'YES'\n(b)'NO'\n(c)'SOMETIMES'",'\n'
    "Do you own more that one scented candle?\n(a) 'YES'\n(b)'NO'\n(c)'SOMETIMES'",'\n'
    "Do you consider yourself a leader?\n (a) 'YES'\n(b)'NO'\n(c)'SOMETIMES'", '\n'
    "Are you a spontaneous person?\n (a) 'YES'\n(b)'NO'\n(c)'SOMETIMES'", '\n'
    "Do you enjoy public speaking?\n (a) 'YES'\n(b)'NO'\n(c)'SOMETIMES'", '\n'
]
name = input("Please enter your name: ").title()
questions = [
    Question(question_prompts[0], "a"),
    Question(question_prompts[1], "b"),
    Question(question_prompts[2], "a"),
    Question(question_prompts[3], "a"),
    Question(question_prompts[4], "b")
              ]
def run_quiz(questions):
     score = 0
     for question in questions:
          answer = input(question.prompt)
          if answer == question.answer:
               score += 1
     print("\n{0}, you scored {1} out of {2}.".format(name, score, len(questions)))
run_quiz(questions)


@app.route("/question/add", methods=["POST"])
def add_question():
    print("test")
    if request.content_type != "application/json":
        print("test two")
        return "Error: Data must be sent as JSON."
    
    post_data = request.get_json()
    print(post_data)
    prompt = post_data.get("prompt")
    answer = post_data.get("answer")
  

    record = (prompt, answer)
    db.session.add(record)
    db.session.commit()

    return jsonify("Data added successfully")

@app.route("/prompt/get", methods=["GET"])
    
    

@app.route("/prompt/get/marshmallow", methods=["GET"])


@app.route("/prompt/update", methods=["PUT"])

   


   





