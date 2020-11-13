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

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prompt = db.Column(db.String, unique=True, nullable=False)
    answer = db.Column(db.String, nullable=False)
    
    

    def __init__(self, prompt, answer):
        self.prompt = prompt
        self.answer = answer
        

class QuestionSchema(ma.Schema):
    class Meta:
        fields = ("id", "prompt", "answer")


question_schema = QuestionSchema()
multiple_questions_schema = QuestionSchema(many=True)
 



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
    

    record = Question(prompt, answer)
    db.session.add(record)
    db.session.commit()

    return jsonify("Data added successfully")

@app.route("/question/get", methods=["GET"])
def get_all_questions():
    all_questions = db.session.query(Question.id, Question.prompt, Question.answer).all()
    return jsonify(all_questions)

@app.route("/question/get/<id>", methods=["GET"])
def get_one_question(id):
    one_question = db.session.query(Question.id, Question.prompt, Question.answer,).filter(Question.id == id).first() 
    return jsonify(one_question)


@app.route("/question/get/marshmallow", methods=["GET"])
def get_all_questions_marshmallow():
   
    all_questions = db.session.query(Question).all()
    return jsonify(multiple_questions_schema.dump(all_questions))


@app.route("/question/get/marshmallow/<id>", methods=["GET"])
def get_one_question_marshmallow(id):
   
    one_question = db.session.query(Question).filter(Question.id == id).first()



    return jsonify(question_schema.dump(one_question))

@app.route("/question/update/<old_prompt>", methods=["PUT"])
def update_question(old_prompt):
    if request.content_type != "application/json":
        return "Error: Data must be sent as JSON."

    put_data = request.get_json()
    prompt = put_data.get("prompt")
    answer = put_data.get("answer")
    

    record = db.session.query(Question).filter(Question.title == old_prompt).first()

    if prompt is not None:
        record.prompt = prompt
    if author is not None:
        record.answer = answer
    


    db.session.commit()
    return jsonify("Data updated successfully")



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



if __name__ == "__main__":
    app.run(debug=True)